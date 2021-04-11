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
            'username': 'wesam',
            'email': 'wesam@gmail.com',
            'password': 'mypass',
        }
        # data for second user
        data2 = {
            'username': 'nadeem',
            'email': 'nadeem@gmail.com',
            'password': 'nadempass',
        }

        # creating users
        self.user = CustomUser.objects._create_user(**data)
        self.user2 = CustomUser.objects._create_user(**data)

        response = self.client.post(self.login_url, data=data)
        result = response.json()
        
        # setting the headers formain user
        self.auth_header = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])
        }

        # upload files to test on later for books images and book files
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())

        data = {
            'file_upload': avatar_file
        }

        self.client.post(self.file_upload_url, data=data, **self.auth_header)

        self.client.post(self.file_upload_url, data=data, **self.auth_header)
        