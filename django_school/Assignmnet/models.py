from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe
from phone_field import PhoneField
from django.utils import timezone
from django.db import models
from classroom.models import User,Student,Teacher


# Create your models here.
class Assignment(models.Model):
    assgn_title=models.CharField(max_length=100,blank=True)
    
    date_posted=models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='documents/',default=True)
    subject = models.CharField(max_length=100,blank=True)
   
    # def save(self,*args,**kwargs):
    #     if not self.id:
    #         self.date_posted=timezone.now()
    #     return super(Assignment, self).save(self,*args,**kwargs)
