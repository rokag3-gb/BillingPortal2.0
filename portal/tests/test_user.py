from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        self.normal_user = User.objects.create_user('test1', 'test1@test.com', '1234qwer!@#$')
        self.super_user = User.objects.create_superuser('test', 'test@test.com', '1234qwer!@#$')

    def test_1(self):
        self.assertEqual(False, self.normal_user.is_superuser)
        self.assertEqual(True, self.super_user.is_superuser)


