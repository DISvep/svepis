from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post
from rest_framework.test import APIClient


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(content='Test post', user=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.content, 'Test post')
        self.assertEqual(self.post.user, self.user)
        self.assertIsNotNone(self.post.date)


class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.post = Post.objects.create(content='Test post', user=self.user)

    def test_post_list_view(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test post')

    def test_post_create_view(self):
        response = self.client.post(reverse('post-create'), {'content': 'New post'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content='New post').exists())

    def test_post_update_view(self):
        response = self.client.post(reverse('post-update', args=[self.post.id]), {'content': 'Updated post'})
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.content, 'Updated post')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post-delete', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())


class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='apipass')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(content='API Test post', user=self.user)

    def test_api_post_list(self):
        response = self.client.get(reverse('post-list-api'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    def test_api_post_create(self):
        response = self.client.post(reverse('post-list-api'), {'content': 'API new post', 'user': self.user.id})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Post.objects.filter(content='API new post').exists())
