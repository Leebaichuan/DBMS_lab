from django.contrib import admin

# Register your models here.
from .models import Subbank, Department, Employee

admin.site.register(Subbank)
admin.site.register(Department)
admin.site.register(Employee)