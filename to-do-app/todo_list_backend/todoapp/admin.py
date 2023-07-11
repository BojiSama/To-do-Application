from django.contrib import admin

from .models import *

# register our task model
admin.site.register(Task)
