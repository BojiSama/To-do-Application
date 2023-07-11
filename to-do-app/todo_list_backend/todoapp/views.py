from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.conf import settings
from django.core.mail import send_mail

from datetime import datetime
from django.utils import timezone

from .models import Task
from .forms import TaskForm

# sign up and create a new user
def signuppage(request):
    if request.method == 'POST':
        # capture all the signup form data
        uname = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        

        # Check if the username is not empty
        if not uname:
            return HttpResponse('Please provide a valid username.')

        # Check if the passwords match
        if password1 != password2:
            return HttpResponse('Passwords do not match.')

        # Create the user
        user = User.objects.create_user(username=uname, email=email, password=password1)
        user.first_name = firstname
        user.last_name = lastname
        user.save() # save the created user

        # send a welcoming email to our new user
        subject = 'welcome to our todo app'
        message = f'Hi {user.username}, thank you for registering with us'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)
        
        # if everything is ok, go to the login page
        return redirect('login')
    return render(request, 'signup.html') # something went wrong :(


# user login
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "bad_login.html")
    return render(request, 'login.html')


# logout a user
def logoutpage(request):
    logout(request)
    return redirect('login')


# to display tasks
@login_required(login_url='login')
def task_list(request):
    if request.method == 'POST':
        task = request.POST.get('task_name') # get a task_name
        new_task = Task(name=task, user=request.user) # create a new task instance
        new_task.save() # add new_task to database
        return redirect("edit_task", pk=new_task.id) # go to the edit page and specify the date and time

    tasks = Task.objects.filter(user=request.user)  # filter out tasks for particular user
    user = request.user # this is the user

    # look for a task that is about to expire
    for task in tasks:
        now = timezone.now() # now
        later = task.future_date # expiration date
        if later is not None and later > now:
            difference = later - now
            hours, remainder = divmod(difference.seconds, 3600) # hours??, unused variable
            minutes, seconds = divmod(remainder, 60) # seconds is also unused
            
            # send an alert email to our user if the is left with only 5 mins to expire
            if minutes < 5:
                subject = 'ALERT!'
                message = f'Hi {user.username}, this is to kindly let you know that "{task.name}" is only left with {minutes} mins to expire'
                email_from = settings.EMAIL_HOST_USER # sender
                recipient_list = [user.email, ] # receiver
                send_mail(subject, message, email_from, recipient_list, fail_silently=False) #send the email

    context = {'user':user, 'tasks':tasks}  # context dictionary
    return render(request, 'index.html', context)  # render index.html


# edit a task
@login_required(login_url='login')
def edit_task(request, pk):
    task = Task.objects.get(id=pk) # get task of with primary key pk
    form = TaskForm(instance=task)  # create a new form for the current task
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task) # post request of the form
        if form.is_valid():
            form.save()
            return redirect('/index') # if form is valid, save it and go to the index page
    user = request.user
    context = {'task':task, 'form':form, 'user':user}
    return render(request, "edit_task.html", context)


# delete a task
@login_required(login_url='login')
def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/index') # if form is valid, save it and go to the index page
    context = {'task':task}
    return render(request, "delete_task.html", context)






