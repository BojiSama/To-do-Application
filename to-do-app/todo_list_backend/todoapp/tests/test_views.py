from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from todoapp.models import Task

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(name='Test Task', user=self.user)

    def test_signuppage(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Check if the new user is created
  
    # ... (other test functions)
    def test_loginpage_successful(self):
      response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
      self.assertEqual(response.status_code, 302)  # Check if the user is redirected after successful login
      self.assertTrue(response.wsgi_request.user.is_authenticated)  # Check if the user is authenticated

    def test_loginpage_unsuccessful(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Check if the user stays on the login page after unsuccessful login
        self.assertFalse(response.wsgi_request.user.is_authenticated)  # Check if the user is not authenticated
    
    def test_logoutpage(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected after successful logout
        self.assertFalse(response.wsgi_request.user.is_authenticated)  # Check if the user is logged out    

    def test_task_list_display(self):
        self.client.login(
          username='testuser', 
          password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  # Check if the task list page is displayed
        self.assertContains(response, 'Test Task')  # Check if the existing task is displayed

    def test_task_list_add_new_task(self):
        self.client.login(
         username='testuser',
         password='testpassword')
        response = self.client.post(reverse('index'), {'task_name': 'New Task'})
        self.assertEqual(response.status_code, 200)  # Check if the task list page is displayed after adding a new task
        self.assertTrue(Task.objects.filter(name='New Task', user=self.user).exists())  # Check if the new task is created
        self.assertContains(response, 'New Task')  # Check if the new task is displayed
    
    def test_delete_task(self):
        self.client.login(
          username='testuser', 
          password='testpassword')
        response = self.client.post(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Check if the user is redirected after successful task deletion
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())  # Check if the task is deleted