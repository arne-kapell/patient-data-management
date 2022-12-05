import uuid
from django.test import TestCase, SimpleTestCase, TransactionTestCase

from pdm.models import User

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


class UserTestCase(TestCase):
    def setUp(self):
        self.credentials = [
            (uuid.uuid4().hex + '@test.domain', uuid.uuid4().hex) for _ in range(10)]

    def test_user_creation(self):
        """Test user creation and deletion"""
        for email, password in self.credentials:
            user = User.objects.create_user(email, password)
            self.assertEqual(user.email, email)
            self.assertTrue(user.check_password(password))
            self.assertTrue(user.is_active)
            self.assertFalse(user.is_staff)
            self.assertFalse(user.is_superuser)
            self.assertFalse(user.verified)
            self.assertEqual(user.role, User.PATIENT)
            user.delete()
            self.assertFalse(User.objects.filter(email=email).exists())

    def test_user_creation_with_role(self):
        """Test user creation with role (doctor, verificator)"""
        for email, password in self.credentials[:2]:
            user = User.objects.create_user(email, password, role=User.DOCTOR)
            self.assertEqual(user.role, User.DOCTOR)
            user.delete()
            self.assertFalse(User.objects.filter(email=email).exists())

        for email, password in self.credentials[2:4]:
            user = User.objects.create_user(
                email, password, role=User.VERIFICATOR)
            self.assertEqual(user.role, User.VERIFICATOR)
            user.delete()
            self.assertFalse(User.objects.filter(email=email).exists())


class RoleTestCase(SimpleTestCase):
    def test_roles(self):
        """Test roles"""
        self.assertEqual(User.PATIENT, 1)
        self.assertEqual(User.DOCTOR, 2)
        self.assertEqual(User.VERIFICATOR, 3)
        self.assertEqual(User.ROLES, (
            (User.PATIENT, 'Patient'),
            (User.DOCTOR, 'Doctor'),
            (User.VERIFICATOR, 'Verificator')
        ))


class LoginTestCase(TransactionTestCase):
    def setUp(self):
        self.credentials = [
            (uuid.uuid4().hex + '@test.domain', uuid.uuid4().hex) for _ in range(10)]
        self.users = [User.objects.create_user(
            email, password) for email, password in self.credentials]

    def test_login(self):
        """Test simple login and logout"""
        for email, password in self.credentials:
            self.client.login(email=email, password=password)
            self.assertTrue(self.client.session.get('_auth_user_id'))
            self.client.logout()
            self.assertFalse(self.client.session.get('_auth_user_id'))

    def test_mail_verification(self):
        """Test mail verification"""
        for user in self.users:
            user = User.objects.get(email=user.email)
            self.assertFalse(user.verified)
            token = default_token_generator.make_token(user)
            user_id_b64 = urlsafe_base64_encode(force_bytes(user.pk))
            response = self.client.get(
                f"/accounts/verify/{user_id_b64}/{token}")
            self.assertEqual(response.status_code, 200)
            user = User.objects.get(email=user.email)
            self.assertTrue(user.verified)

    def test_mail_verification_with_wrong_token(self):
        """Test mail verification with wrong token"""
        for user in self.users:
            user = User.objects.get(email=user.email)
            self.assertFalse(user.verified)
            token = default_token_generator.make_token(user)
            user_id_b64 = urlsafe_base64_encode(force_bytes(user.pk))
            response = self.client.get(
                f"/accounts/verify/{user_id_b64}/{token}1")
            self.assertEqual(response.status_code, 200)
            user = User.objects.get(email=user.email)
            self.assertFalse(user.verified)
