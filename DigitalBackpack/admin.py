from django.contrib import admin
from . models import Class

# Adds the 'Class' model into the application's list of models on the admin site ('/admin/')
admin.site.register(Class)

