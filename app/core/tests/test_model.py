from unittest import TestLoader
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    
    def test_create_user_with_email_success(self):
        """Test creating a new user with email is successful"""
        email = "'test@testdev.com"
        password = 'pass5word'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        
        
    def test_new_user_email_normalized(self):
        """Test the user email is normalized"""
        email = 'test@TESTDEV.COM'
        user = get_user_model().objects.create_user(email, 'test@pass')
        
        self.assertEqual(user.email, email.lower())
        

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "testpass")
            
            
    def test_create_new_superuser(self):
        """Test creating a new superuser
        """
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'super_admin'
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)