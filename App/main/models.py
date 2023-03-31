from django.db import models

class Users(models.Model):
    id = models.IntegerField(primary_key=True, serialize=True, null=False)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(max_length=80, null=False)