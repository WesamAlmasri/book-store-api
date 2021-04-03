from rest_framework.test import APITestCase
from .utils import JWTToken

class TestGenericFunctions(APITestCase):

    def test_get_random(self):
        rand1 = JWTToken.get_random(10)
        rand2 = JWTToken.get_random(10)
        rand3 = JWTToken.get_random(15)

        self.assertTrue(rand1)
        self.assertNotEqual(rand1, rand2)
        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)
    
    def test_get_access_token(self):
        payload = {
            'id': 1
        }

        token = JWTToken.get_access(payload)
        
        self.assertTrue(token)
    
    def test_get_refresh_token(self):
        refresh = JWTToken.get_refresh()
        
        self.assertTrue(refresh)

