from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpage, name='login'), # login url
    path('signup/', views.signuppage, name='signup'), # signup url
    path('index/', views.task_list, name='index'), # index url
    path('edit_task/<int:pk>/', views.edit_task, name='edit_task'), # edit_task url
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'), # delete_task url
    path('logout/', views.logoutpage, name='logout'), # logout url
    path('index/edit_task/<int:pk>/', views.edit_task, name='edit_new'), # new task edit
]




