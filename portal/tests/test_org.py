from django.test import TestCase
from django.contrib.auth.models import User

class OrganizationTestCase(TestCase):
    def setUp(self):
        self.normal_user = User.objects.create_user('test1', 'test1@test.com', '1234qwer!@#$')
        self.super_user = User.objects.create_superuser('test', 'test@test.com', '1234qwer!@#$')
        # self.test_org = Organization.objects.create()

    #     self.test_org.

    # def test_0(self):
