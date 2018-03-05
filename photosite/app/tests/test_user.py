from rest_framework.test import APITestCase

from app.models.user import User, Company


class AdminAuthTestCase(APITestCase):
    def setUp(self):
        self.username = "test_admin"
        self.email = "test@admin.com"
        self.password = "TestPassword"
        self.admin = User.objects.create_superuser(username = self.username,
                                                   password = self.password,
                                                   email = self.email)

        self.company, created = Company.objects.get_or_create(name = 'admin')

        self.admin.company = self.company
        self.admin.save()

        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION = 'JWT {}'.format(self.admin.token))

    def test_user_register(self):
        response = self.client.post('/register', {'username': 'test_user',
                                                  'password': 'test_password',
                                                  'confirm_password': 'test_password',
                                                  'email': 'test@user.com'})
        self.assertEquals(201, response.status_code)


    def test_user_login(self):
        response = self.client.post("/login", {'username': self.username, 'password': self.password})
        data = response.data

        self.assertTrue(200, response.status_code)
        self.assertEquals(data['company']['name'], 'admin')
        self.assertEquals(data['email'], self.admin.email)
        self.assertEquals(data['username'], self.admin.username)

    def test_user_logout(self):
        response = self.client.post('/logout')
        self.assertTrue(204, response.status_code)

        test_admin = User.objects.get(username = self.username)
        self.assertEquals('', test_admin.token)