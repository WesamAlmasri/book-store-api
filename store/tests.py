from rest_framework.test import APITestCase
from .models import Category, Auther, Book, BookImage, BookComment
from user.models import CustomUser
from user.tests import create_image
from django.core.files.uploadedfile import SimpleUploadedFile

class TestBookInfo(APITestCase):
    file_upload_url = '/user/file-upload'
    login_url = '/user/login'
    categories_url = '/store/categories'
    authers_url = '/store/authers'
    book_url = '/store/book'
    book_image_url = '/store/book-image'
    book_comment_url = '/store/book-comment'

    def setUp(self):
        # data for main user
        data = {
            'username': 'wesamco',
            'email': 'wesamco@gmail.com',
            'password': 'mypassenw',
        }

        # data for second user
        data2 = {
            'username': 'nadeemco',
            'email': 'nadeemco@gmail.com',
            'password': 'nadempass',
        }

        # creating users
        self.user = CustomUser.objects._create_user(**data)
        self.user2 = CustomUser.objects._create_user(**data2)

        response = self.client.post(self.login_url, data=data)
        result = response.json()
        
        # setting the headers for main user
        self.auth_header = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])
        }

        # creating some categories
        Category.objects.create(name='Electronics')
        Category.objects.create(name='Sport')
        Category.objects.create(name='Math')

        # upload files to test on later for books images and book files
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())

        data = {
            'file_upload': avatar_file
        }

        self.client.post(self.file_upload_url, data=data, **self.auth_header)

        self.client.post(self.file_upload_url, data=data, **self.auth_header)
    
    def test_get_categories(self):

        response = self.client.get(self.categories_url, **self.auth_header)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['name'], 'Electronics')
        self.assertEqual(result[2]['id'], 3)
        self.assertEqual(result[2]['name'], 'Math')
    
    def test_post_create_auther(self):
        data = {
            'name': 'Auther1',
        }
    
        response = self.client.post(self.authers_url, data, **self.auth_header)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['name'], 'Auther1')
        self.assertEqual(result['user']['id'], 1)

    def test_put_update_auther(self):
        data = {
            'name': 'Auther1',
        }
    
        response = self.client.post(self.authers_url, data, **self.auth_header)
        result = response.json()

        data = {
            'name': 'Auther11',
        }
    
        response = self.client.put(f"{self.authers_url}/{result['id']}", data, **self.auth_header)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['name'], 'Auther11')
        self.assertEqual(result['user']['id'], 1)
    
    def test_delete_auther(self):
        data = {
            'name': 'Auther1',
        }
    
        response = self.client.post(self.authers_url, data, **self.auth_header)
        result = response.json()

        response = self.client.delete(f"{self.authers_url}/{result['id']}", data, **self.auth_header)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(result['error'])
    
