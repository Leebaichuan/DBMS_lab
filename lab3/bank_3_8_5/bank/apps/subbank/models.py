from django.db import models

# Subbank(Name,City,Asset) where Name is primary key
class Subbank(models.Model):
    Name = models.CharField(max_length = 255, primary_key = True)
    City = models.CharField(max_length = 255)
    Asset = models.DecimalField(max_digits = 20, decimal_places = 2)

    def __str__(self):
        return self.Name

# the entity of a department in a subbank
class Department(models.Model):
    ID = models.CharField(max_length = 20,primary_key = True)
    Name = models.CharField(max_length = 255)
    Type = models.CharField(max_length = 20)
    Leader_ID = models.CharField(max_length = 20)
    Subbank = models.ForeignKey(Subbank, \
        related_name = 'belongs_to',on_delete = models.CASCADE)

    def __str__(self):
        return self.ID

# the entity of an employee in a department
# each employee has a unique ID
# and has a Department_ID of the department that he/she works for
class Employee(models.Model):
    ID = models.CharField(max_length = 20,primary_key = True)
    Name = models.CharField(max_length = 255)
    PhoneNum = models.CharField(max_length = 20)
    Address = models.CharField(max_length = 255)
    StartDate = models.DateTimeField(auto_now_add = True)
    Depart = models.ForeignKey(Department, \
        related_name = 'works_for',on_delete = models.CASCADE)

    def __str__(self):
        return self.ID