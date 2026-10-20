
from rest_framework import serializers
from django.db import models
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
     # @property
     # def created_at(self):
     #   return self.date_joined
     class Role(models.TextChoices):
         ADMIN="ADMIN","admin",
         MANAGER="MANAGER","manager",
         EMPLOYEE= "EMPLOYEE","employee"
     class Department(models.TextChoices):
        INFRA="INFRA",'infra',
        DEVELOPMENT="DEVELOPMENT",'development',
        QA="QA",'qa',
        HR="HR",'hr',
        

     
     employee_name=models.CharField(max_length=100)

  
     emp_id=models.IntegerField(unique=True,null=True)
     departmet=models.CharField(max_length=100,choices=Department.choices,default=Department.INFRA)
     joining_date=models.DateField(null=True)
     role=models.CharField(max_length=100,choices=Role.choices,default=Role.EMPLOYEE)
     date_joined = models.DateTimeField(default=timezone.now,db_column="created_at")
     manager_id=models.ForeignKey('self',on_delete=models.SET_NULL,null=True,related_name="manager")

     class Meta:

      constraints=[
          models.UniqueConstraint(fields=['email'],name='unique_email')

     ]
     
     USERNAME_FIELD = "email"
     REQUIRED_FIELDS = []
    
     
     def __str__(self):
          print("the instance method actually called")
          return self.username



     
     