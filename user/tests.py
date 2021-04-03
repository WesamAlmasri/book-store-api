from rest_framework.test import APITestCase
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

    