import datetime
import uuid
from django.test import TestCase, SimpleTestCase, TransactionTestCase, LiveServerTestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from pdm.models import AccessRequest, User, Document

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


# class StressTestTokenGenerator(TestCase):
#     def test_token_generator_with_verification_endpoint(self):
#         """Test token generator with verification endpoint"""
#         for _ in range(100):
#             user = User.objects.create_user(
#                 email=uuid.uuid4().hex + '@test.domain', password=uuid.uuid4().hex)
#             token = default_token_generator.make_token(user)
#             user_id_b64 = urlsafe_base64_encode(force_bytes(user.pk))
#             response = self.client.get(
#                 f"/accounts/verify/{user_id_b64}/{token}")
#             self.assertEqual(response.status_code, 200)
#             user = User.objects.get(email=user.email)
#             self.assertTrue(user.verified)
#             user.delete()


class AccessRequestTestCase(TestCase):
    def setUp(self):
        self.user_a_creds = {
            'email': uuid.uuid4().hex + '@test.domain',
            'password': uuid.uuid4().hex
        }
        self.user_b_creds = {
            'email': uuid.uuid4().hex + '@test2.domain',
            'password': uuid.uuid4().hex
        }
        self.user_a = User.objects.create_user(**self.user_a_creds)
        self.user_b = User.objects.create_user(**self.user_b_creds)

    def test_access_request_creation(self):
        """Test access request creation"""
        self.client.login(email=self.user_a.email,
                          password=self.user_a.password)
        request = AccessRequest.objects.create(
            patient=self.user_b, requested_by=self.user_a, period_start=datetime.date.today(), period_end=datetime.date.today())
        self.assertEqual(request.patient, self.user_b)
        self.assertEqual(request.requested_by, self.user_a)
        self.assertFalse(request.approved)
        self.assertFalse(request.denied)
        self.user_a.delete()
        self.client.logout()
        request.delete()
    
    
    def test_uploadFileTest(self):
        self.assertTrue(self.client.login(**self.user_a_creds))
        file = SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf")
        response = self.client.post('/upload/', {'form': {'file': file}})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    
    def test_viewOwnDocument(self):
        self.assertTrue(self.client.login(**self.user_a_creds))
        doc = Document.objects.create(owner=self.user_a, file=SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf"))
        response = self.client.get("/preview/" + str(doc.uid))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
    
    def test_viewSomeoneElsesDocument(self):
        """T1, T3: Test view someone else's document without permission"""
        self.assertTrue(self.client.login(**self.user_a_creds))
        doc = Document.objects.create(owner=self.user_a, file=SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf"))
        self.client.logout()
        self.assertTrue(self.client.login(**self.user_b_creds))
        response = self.client.get("/preview/" + str(doc.uid))
        self.assertEqual(response.status_code, 403)
        self.client.logout()



class ProfileDataTestcase(LiveServerTestCase):
    def setUp(self):
        self.credentials = {
            'email': uuid.uuid4().hex + '@test.domain',
            'password': uuid.uuid4().hex
        }
        self.user = User.objects.create_user(
            self.credentials['email'], self.credentials['password'])
        self.user.first_name = 'Max'
        self.user.last_name = 'Mustermann'
        self.user.save()
        self.client = Client()
    
    def test_profile_data_with_login(self):
        """T1, T2: Test profile data with login"""
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].first_name, 'Max')
        self.assertEqual(response.context['user'].last_name, 'Mustermann')
        self.client.logout()
    
    def test_profile_data_without_login(self):
        """T1, T2: Test profile data without login"""
        response = self.client.get('/profile/')
        self.assertEqual(response.url, '/accounts/login/?next=/profile/')

class SQLInjectionTestCase(TestCase):
    def setUp(self):
        self.credentials = {
            'email': uuid.uuid4().hex + '@test.domain',
            'password': uuid.uuid4().hex
        }
        self.user = User.objects.create_user(**self.credentials)
        self.client = Client()
    
    def test_sql_injection(self):
        """T5: Test SQL injection with document preview"""
        self.assertTrue(self.client.login(**self.credentials))
        doc = Document.objects.create(owner=self.user, file=SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf"))
        response = self.client.get("/preview/" + str(doc.uid) + "' OR 1=1")
        self.assertEqual(response.status_code, 400)
        self.client.logout()

class XSSInjectionTestCase(LiveServerTestCase):
    def setUp(self):
        self.credentials = {
            'email': uuid.uuid4().hex + '@test.domain',
            'password': uuid.uuid4().hex
        }
        self.user = User.objects.create_user(**self.credentials)
        self.client = Client()
    
    def test_xss_injection(self):
        """T7: Test XSS injection with document description"""
        self.assertTrue(self.client.login(**self.credentials))
        Document.objects.create(owner=self.user, file=SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf"), description="<script>alert('XSS')</script>")
        response = self.client.get("/docs/")
        self.assertNotContains(response, "<script>alert('XSS')</script>")
        self.client.logout()

class StressTestDatabase(LiveServerTestCase):
    def setUp(self):
        self.credentials = {
            'email': uuid.uuid4().hex + '@test.domain',
            'password': uuid.uuid4().hex
        }
        self.user = User.objects.create_user(**self.credentials)
        self.client = Client()
    
    def test_stress_test_database(self):
        """T8: Test stress test database"""
        self.assertTrue(self.client.login(**self.credentials))
        for _ in range(1000):
            Document.objects.create(owner=self.user, file=SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf"))
        self.client.logout()

class TestAdminLogin(LiveServerTestCase):
    def setUp(self):
        self.credentials = {
            'email': uuid.uuid4().hex + '@test.domain',
            'password': uuid.uuid4().hex
        }
        self.user = User.objects.create_user(**self.credentials)
        self.client = Client()
    
    def test_admin_login(self):
        """T9: Test admin login"""
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/login/?next=/admin/')
        self.client.logout()
    
    def test_admin_login_with_superuser(self):
        """T9: Test admin login with superuser"""
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.assertTrue(self.client.login(**self.credentials))
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()