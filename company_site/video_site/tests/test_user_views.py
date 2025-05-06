from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_page') 
        self.login_url = reverse('login_page')      
        self.logout_url = reverse('logout_view')    
        self.home_url = "/"

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_forms/register.html')

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_forms/login.html')

    def test_login_post_invalid(self):
        data = {'username': 'ghost', 'password': 'wrong'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_forms/login.html')
        self.assertContains(response, "Please enter a correct username and password")

    def test_logout_view(self):
        user = User.objects.create_user(username='tester', password='testpass123')
        self.client.login(username='tester', password='testpass123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, self.home_url)