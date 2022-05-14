from audioop import add
from django.test import TestCase

from app.calc import add, subtract


class CalcTest(TestCase):
    def test_add_two_numbers(self):
        """
        Test that two numbers are added together
        """
        
        self.assertNotEqual(add(3,8), 78)
        self.assertEqual(add(3,6), 9)
        self.assertEqual(add(3,8), 11)
        
    def test_subtract_two_numbers(self):
        """
        Test to subtract two numbers and return value
        """
        
        self.assertEqual(subtract(3,1), 2)