from django.test import TestCase
from .models import Account
from django.urls import reverse
from django.test import SimpleTestCase

class CustomUserTests(TestCase):
    def test_create_user(self): 
        User = Account() 
        user = User.objects.create_user( 
            email='foyle@gmail.com', 
            firstname='Gilfoyle',
            lastname='SonOfAnton' 
             
        ) 
        self.assertEqual(user.firstname, 'Gilfoyle'),
        self.assertEqual(user.lastname, 'SonOfAnton'), 
        self.assertEqual(user.email, 'folyle@gmail.com') 
        self.assertTrue(user.is_active) 
        self.assertFalse(user.is_staff) 
        self.assertFalse(user.is_superuser)

def test_create_superuser(self): 
    User = Account()
    admin_user = User.objects.create_superuser( 
        firstname='superadmin',
        lastname='Supernova',
        email='superadmin@gmail.com',  
    ) 
    self.assertEqual(admin_user.firstname, 'superadmin')
    self.assertEqual(admin_user.lastname, 'Supernova') 
    self.assertEqual(admin_user.email, 'superadmin@gmail.com') 
    self.assertTrue(admin_user.is_active) 
    self.assertTrue(admin_user.is_staff) 
    self.assertTrue(admin_user.is_superuser)

class HomePageTest(SimpleTestCase):
    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.asserteEqual(response.status_code, 200)

    def homepage_url_name_test(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)