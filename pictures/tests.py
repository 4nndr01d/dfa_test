import json
import tempfile

from PIL import Image
import mock
from django.core.files import File
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from pictures.models import Picture


class PicturesAPIViewTestCase(APITestCase):
    user_data = {
        "username": 'testuser',
        "password": '12345',
    }
    admin_data = {
        "username": 'admin',
        "password": '12345',
    }

    def setUp(self) -> None:
        self.admin = User.objects.create_user(username=self.admin_data['username'], password=self.admin_data['password'],
                                              is_superuser=True, is_staff=True)
        self.user = User.objects.create_user(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.post(reverse("token_obtain"), {
            "username": self.user_data['username'],
            "password": self.user_data['password'],
        })
        self.token = json.loads(response.content)['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        img = mock.MagicMock(spec=File, name='FileMock')
        img.name = 'test1.jpg'

        self.picture = Picture.objects.create(title='test', file=img, user=self.user)

    def test_get_pictures(self):
        response = self.client.get(reverse("pictures-list"))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['results'][0]['id'], self.picture.id)
        self.assertEqual(data['results'][0]['title'], self.picture.title)

    def test_create_picture(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)

        with open(tmp_file.name, 'rb') as data:
            response = self.client.post(reverse("pictures-list"), {"file": data, "title": 'Test'}, format='multipart')
            response_data = json.loads(response.content)
            self.assertEqual(201, response.status_code)
            self.assertTrue('id' in response_data)
            self.assertTrue('title' in response_data)
            self.assertTrue('file' in response_data)

    def test_retrieve_picture(self):
        response = self.client.get(reverse("pictures-detail", args=[self.picture.id]))
        response_data = json.loads(response.content)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.picture.title, response_data['title'])

    def test_update_picture(self):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)

        with open(tmp_file.name, 'rb') as data:
            response = self.client.put(reverse("pictures-detail", args=[self.picture.id]),
                                       {"file": data, "title": 'Test123'}, format='multipart')
            response_data = json.loads(response.content)
            self.assertEqual(200, response.status_code)
            self.assertEqual('Test123', response_data['title'])

    def test_delete_picture(self):
        response = self.client.delete(reverse("pictures-detail", args=[self.picture.id]))
        self.assertEqual(204, response.status_code)

    def test_delete_all_pictures_by_user(self):
        response = self.client.delete(reverse("pictures-delete-all"))
        self.assertEqual(403, response.status_code)

    def test_delete_all_pictures_by_admin(self):
        response = self.client.post(reverse("token_obtain"), {
            "username": self.admin_data['username'],
            "password": self.admin_data['password'],
        })
        token = json.loads(response.content)['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.delete(reverse("pictures-delete-all"))
        self.assertEqual(204, response.status_code)
