from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from todoapp.views import signuppage, loginpage, logoutpage, task_list, delete_task, edit_task
from todoapp.models import Task
from django.contrib.auth import get_user_model

class TestUrls(SimpleTestCase):
  
  def test_login(self):
    url = reverse('login')
    self.assertEquals(resolve(url).func, loginpage)

  def test_signup(self):
    url = reverse('signup')
    self.assertEquals(resolve(url).func, signuppage)  

  def test_logout(self):
    url = reverse('logout')
    self.assertEquals(resolve(url).func, logoutpage)  
  
  def test_index(self):
    url = reverse('index')
    self.assertEquals(resolve(url).func, task_list)

class BlogTest(TestCase): 
  def setUp(self):
    self.user = get_user_model().objects.create_user(username='test', password='pass')
    self.my_object = Task.objects.create(
      name = 'task',
      user = self.user
    )
  def test_taskdeletion(self):
    url = reverse('delete_task',args=[self.my_object.pk])
    self.assertEquals(resolve(url).func, delete_task)   

  def test_taskupdate(self):
    url = reverse('edit_task', args=[self.my_object.pk]) 
    self.assertEquals(resolve(url).func, edit_task)   