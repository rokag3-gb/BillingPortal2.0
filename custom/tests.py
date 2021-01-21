from custom.models import User
from django.test import TestCase, Client
from django.urls import reverse

from custom.models import Org
from custom.services import SESSION_ORGANIZATION


class OrgUserTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='user_1', password='pw_user_1')
        self.user_2 = User.objects.create_user(username='user_2', password='pw_user_2')
        self.org_1 = Org.objects.create(name='org_1', slug='org1')
        self.org_2 = Org.objects.create(name='org_2', slug='org2')

    def test_001(self):
        """
        맴버추가 기능을 테스트 한다.
        """
        self.assertFalse(self.org_1.is_member(user=self.user_1))
        self.assertFalse(self.org_1.is_member(user=self.user_2))
        self.assertFalse(self.org_2.is_member(user=self.user_1))
        self.assertFalse(self.org_2.is_member(user=self.user_2))

        self.org_1.add_user(user=self.user_1)
        self.org_2.add_user(user=self.user_2)

        self.assertTrue(self.org_1.is_member(user=self.user_1))
        self.assertFalse(self.org_1.is_member(user=self.user_2))
        self.assertFalse(self.org_2.is_member(user=self.user_1))
        self.assertTrue(self.org_2.is_member(user=self.user_2))


class OrgSessionTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(username='user_1', password='pw_user_1')
        self.user_2 = User.objects.create_user(username='user_2', password='pw_user_2')
        self.org_1 = Org.objects.create(name='org_1', slug='org1')
        self.org_1.add_user(user=self.user_1)
        self.org_2 = Org.objects.create(name='org_2', slug='org2')

    def test_001(self):
        """
        로그인 한 뒤 원하는 org 로 선택할 수 있는지 확인한다.
        """
        c = Client()
        c.login(username='user_1', password='pw_user_1')
        c.get(path='/organization/switch_to/org_1')

        self.assertEqual(self.org_1.slug, c.session[SESSION_ORGANIZATION])

        c = Client()
        c.login(username='user_2', password='pw_user_2')
        c.get(path='/organization/switch_to/org_1')

        self.assertIsNone(None, c.session.get(SESSION_ORGANIZATION, None))

    def test_002(self):
        """
        로그인 한 뒤 org 가 여러개라면 org 를 선택하는 페이지로 이동한다.
        """
        self.org_2.add_user(user=self.user_1)

        c = Client()
        c.login(username='user_1', password='pw_user_1')
        response = c.get(reverse('list-org'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organizations/list.html')

    def test_003(self):
        """
        로그인 한 뒤 org 가 하나라면 자동으로 선택되게 한다.
        """
        c = Client()
        c.login(username='user_1', password='pw_user_1', follow=True)
        response = c.get(reverse('list-org'), follow=True)

        self.assertEqual(self.org_1.slug, c.session[SESSION_ORGANIZATION])
        self.assertTupleEqual((reverse('dashboard'), 302), response.redirect_chain[-1])

    def test_004(self):
        """
        org가 연결된 것이 없으면 org 선택 화면에서 머무르게 한다.
        """
        c = Client()
        c.login(username='user_2', password='pw_user_2', follow=True)
        response = c.get(reverse('dashboard'), follow=True)

        self.assertTupleEqual((reverse('list-org'), 302), response.redirect_chain[-1])

    def test_005(self):
        """
        org가 2개 이상이여도 자동으로(가장 처음것)으로 org를 선택하여 로그인 한다.
        """
        self.org_2.add_user(user=self.user_1)
        self.org_2.add_user(user=self.user_2)
        self.org_1.add_user(user=self.user_2)

        c = Client()
        c.login(username='user_1', password='pw_user_1', follow=True)
        response = c.get(reverse('dashboard'), follow=True)

        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()
        self.assertEqual(self.org_1, self.user_1.org_last_selected)
        self.assertEqual(self.org_1.slug, c.session[SESSION_ORGANIZATION])

        c = Client()
        c.login(username='user_2', password='pw_user_2', follow=True)
        response = c.get(reverse('dashboard'), follow=True)

        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()
        self.assertEqual(self.org_2, self.user_2.org_last_selected)
        self.assertEqual(self.org_2.slug, c.session[SESSION_ORGANIZATION])

    def test_006(self):
        """
        로그인 이후 org 가 삭제되었을 때 새롭게 지정된 org 로 다시 변경될 수 있게 한다.
        """
        c = Client()
        c.login(username='user_1', password='pw_user_1', follow=True)
        response = c.get(reverse('dashboard'), follow=True)
        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()

        self.assertEqual(self.org_1, self.user_1.org_last_selected)
        self.assertEqual(self.org_1.slug, c.session[SESSION_ORGANIZATION])

        # INFO: 오너쉽이 있는 user 삭제 문제로 org 삭제만 테스트 함
        self.org_2.add_user(user=self.user_1)
        self.org_1.is_active = False
        self.org_1.save(update_fields=['is_active'])

        response = c.get(reverse('dashboard'), follow=True)
        self.user_1.refresh_from_db()
        self.user_2.refresh_from_db()

        self.assertEqual(self.org_2.slug, c.session[SESSION_ORGANIZATION])
        self.assertEqual(self.org_2, self.user_1.org_last_selected)

