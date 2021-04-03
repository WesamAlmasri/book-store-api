from rest_framework.test import APITestCase
from .models import CustomUser, UserProfile
from .utils import JWTToken
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from six import BytesIO
from PIL import Image

def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    data = BytesIO();
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)

    if not storage:
        return data

    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)

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

class TestFileUpload(APITestCase):
    file_upload_url = '/user/file-upload'

    def test_file_upload(self):
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front1.png', avatar.getvalue())
        data = {
            'file_upload': avatar_file
        }

        response = self.client.post(self.file_upload_url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['id'], 1)


class TestAuth(APITestCase):
    login_url = '/user/login'
    register_url = '/user/register'
    refresh_url = '/user/refresh'

    def test_register(self):
        data = {
            'username': 'wesam',
            'email': 'wesam@gmail.com',
            'password': 'mypass',
        }

        response = self.client.post(self.register_url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, 201)
    
    def test_login(self):
        data = {
            'username': 'wesam',
            'email': 'wesam@gmail.com',
            'password': 'mypass',
        }

        self.client.post(self.register_url, data=data)

        response = self.client.post(self.login_url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(result['access'])
        self.assertTrue(result['refresh'])
    
    def test_refresh(self):
        data = {
            'username': 'wesam',
            'email': 'wesam@gmail.com',
            'password': 'mypass',
        }

        self.client.post(self.register_url, data=data)

        response = self.client.post(self.login_url, data=data)
        refresh = response.json()['refresh']

        response = self.client.post(self.refresh_url, data={'refresh': refresh})
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(result['access'])
        self.assertTrue(result['refresh'])
    
class TestUserInfo(APITestCase):
    profile_url = '/user/profile'
    file_upload_url = '/user/file-upload'
    login_url = '/user/login'

    def setUp(self):
        data = {
            'username': 'wesam',
            'email': 'wesam@gmail.com',
            'password': 'mypass',
        }

        self.user = CustomUser.objects._create_user(**data)

        response = self.client.post(self.login_url, data=data)
        result = response.json()

        self.auth_header = {
            'HTTP_AUTHORIZATION': 'jocobr {}'.format(result['access'])
        }
    
    def test_post_user_profile(self):
        data = {
            'user_id': self.user.id,
            'first_name': 'Wesam',
            'last_name': 'Al-Masri',
        }

        response = self.client.post(self.profile_url, data=data, **self.auth_header)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['first_name'], 'Wesam')
        self.assertEqual(result['last_name'], 'Al-Masri')
        self.assertEqual(result['user']['username'], 'wesam')

    def test_post_user_profile_with_profile_picture(self):
    
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())

        data = {
            'file_upload': avatar_file
        }

        response = self.client.post(self.file_upload_url, data=data, **self.auth_header)
        result = response.json()

        data = {
            'user_id': self.user.id,
            'first_name': 'Wesam',
            'last_name': 'Al-Masri',
            'profile_picture_id': result['id']
        }
 
        response = self.client.post(self.profile_url, data=data, **self.auth_header)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['first_name'], 'Wesam')
        self.assertEqual(result['last_name'], 'Al-Masri')
        self.assertEqual(result['user']['username'], 'wesam')
        self.assertEqual(result['profile_picture']['id'], 1)
        
    def test_update_user_profile(self):
        data = {
            'user_id': self.user.id,
            'first_name': 'Wesam',
            'last_name': 'Al-Masri',
        }

        response = self.client.post(self.profile_url, data=data, **self.auth_header)
        result = response.json()

        data = {
            'first_name': 'Wesam123',
            'last_name': 'Al-Masri123',
        }

        response = self.client.patch(self.profile_url + f"/{result['id']}", data=data, **self.auth_header)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['first_name'], 'Wesam123')
        self.assertEqual(result['last_name'], 'Al-Masri123')
        self.assertEqual(result['user']['username'], 'wesam')
    
    def test_user_search(self):
    
        UserProfile.objects.create(user=self.user, first_name='Wesam', last_name='Al-Masri')

        user2 = CustomUser.objects._create_user(
            username='nadeem', email='nadeem@gmail.com', password='nadeempassword')
        UserProfile.objects.create(user=user2, first_name='Nadeem', last_name='Rawhi')

        user3 = CustomUser.objects._create_user(
            username='waseem', email='waseem@gmail.com', password='waseempassword')
        UserProfile.objects.create(user=user3, first_name='Waseem', last_name='Rawhi')

        # test keyword = wesam al-masri
        url = self.profile_url + '?keyword=wesam al-masri'

        response = self.client.get(url, **self.auth_header)
        result = response.json()['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 0)

        # test keyword = nadeem
        url = self.profile_url + '?keyword=nadeem'

        response = self.client.get(url, **self.auth_header)
        result = response.json()['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['user']['username'], 'nadeem')

        # test keyword = rawhi
        url = self.profile_url + '?keyword=rawhi'

        response = self.client.get(url, **self.auth_header)
        result = response.json()['results']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['user']['username'], 'nadeem')
        self.assertEqual(result[1]['user']['username'], 'waseem')