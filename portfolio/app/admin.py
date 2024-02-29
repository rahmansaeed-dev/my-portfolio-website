from django.contrib import admin
from .models import CustomModel, Contact
# Register your models here.

@admin.register(CustomModel)
class CustomModelAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','password','phonenumber']

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','email','subject','message']

