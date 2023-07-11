from django.test import TestCase
from django.contrib.auth.models import User
from todoapp.models import Task

class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            user=self.user,
            name='Test Task',
            description='This is a test task',
            complete=False,
            due_date='2023-12-31',
            time='12:00:00',
            future_date='2023-12-31 12:00:00'
        )

    def test_task_creation(self):
        self.assertEqual(self.task.user, self.user)  # Check if the user is set correctly
        self.assertEqual(self.task.name, 'Test Task')  # Check if the name is set correctly
        self.assertEqual(self.task.description, 'This is a test task')  # Check if the description is set correctly
        self.assertFalse(self.task.complete)  # Check if the complete field is set to False by default
        self.assertEqual(str(self.task), 'Test Task')  # Check if the __str__ method returns the task name