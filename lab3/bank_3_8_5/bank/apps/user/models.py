# apps/user/models.py
# relational schema for user
from django.db import models

# the model of User in a bank
class User(models.Model):
    ID = models.CharField(max_length = 20, primary_key = True)
    Name = models.CharField(max_length = 255)
    PhoneNum = models.CharField(max_length = 20)
    Address = models.CharField(max_length = 255)
    Contact_Name = models.CharField(max_length = 255)
    Contact_PhoneNum = models.CharField(max_length = 20)
    Contact_Email = models.EmailField()
    def __str__(self):
        return self.ID
