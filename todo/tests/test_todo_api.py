from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Todo

from todo.serializers import TodoSerializer
from datetime import datetime

TODOS_URL = reverse('todo:todo-list')


def detail_url(todo_id):
    """Return todo detail URL"""
    return reverse('todo:todo-detail', args=[todo_id])


def sample_todo(user, **params):
    """Create and return a sample todo"""
    defaults = {
        'task': 'Sample todo'
    }

    defaults.update(params)

    return Todo.objects.create(user=user, **defaults)


class PublicTodoApiTests(TestCase):
    """Test publicly available todos API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(TODOS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoApiTests(TestCase):
    """Test authorized todo API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testmail@gmail.com',
            'passfau13'
        )
        self.client.force_authenticate(self.user)


    def test_retrieve_todos(self):
        """Test retrieving todos"""
        sample_todo(user=self.user)
        sample_todo(user=self.user, task="New sample task")

        res = self.client.get(TODOS_URL)

        todos = Todo.objects.all().order_by('id')
        serializer = TodoSerializer(todos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)


    def test_todos_limited_to_user(self):
        """Test retrieving todos for user"""

        user2 = get_user_model().objects.create_user(
            'test@gmail.com',
            'pasfaiwfaf'
        )

        sample_todo(user=user2)
        sample_todo(user=self.user)

        res = self.client.get(TODOS_URL)

        todos = Todo.objects.filter(user=self.user)
        serializer = TodoSerializer(todos, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)


    def test_view_todo_detail(self):
        """Test viewing a todo detail"""
        todo = sample_todo(user=self.user)

        url = detail_url(todo.id)
        res = self.client.get(url)

        serializer = TodoSerializer(todo)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_create_todo(self):
        """Test creating todo"""
        payload = {
            'task': 'New Task',
        }

        res = self.client.post(TODOS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_update_todo(self):
        """Test updating a todo with patch"""
        todo = sample_todo(user=self.user)

        paylaod = {
            'task': 'Updated Task',
        }

        url = detail_url(todo.id)
        self.client.patch(url, paylaod)

        todo.refresh_from_db()

        self.assertEqual(todo.task, paylaod['task'])
