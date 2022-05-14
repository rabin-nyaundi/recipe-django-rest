from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSite(TestCase):
    """create superuser and normal user before each test runs"""
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@testdev.com',
            password = 'pass5word'
        )
        
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@testdev.com',
            password = 'pass123',
            name = "test user"
        )
        
    
    def test_user_listed(self):
        """Tests that users are created on a user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        
    
    def test_user_change_page(self):
        """Test that the user edit page is working"""
        url = reverse('admin:core_user_change',args=[self.user.id])
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)
        
        
    def test_create_user_page(self):
        """Test that user create page is working correctly"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        
        self.assertEqual(res.status_code, 200)