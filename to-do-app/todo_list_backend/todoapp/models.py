from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user as a foreign key
    name = models.CharField(max_length=100) # task name
    description = models.TextField(null=True, blank=True) # description
    complete = models.BooleanField(default=False) # task completion flag
    created = models.DateTimeField(auto_now_add=True) # date the task was created
    due_date = models.DateField(null=True) # the date the task should be completed
    time = models.TimeField(null=True) # the time ... ditto
    future_date = models.DateTimeField(null=True) # complete date and time, filled in automatically
                                                # after filling in the date and time fields in the form

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-future_date"] # set ordering by future date, in descending order
