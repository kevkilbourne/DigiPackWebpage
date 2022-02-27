from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    # The name of the class is a String
    classname = models.CharField(max_length=50)

    # Makes the instructor a 'User' and on deletion of the class, the instructor
    # is also deleted ('on_delete=models.CASCADE')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)

    # When a class is called in Python shell, it will display the Class's classname
    def __str__(self):
        return self.classname

