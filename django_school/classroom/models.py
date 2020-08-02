from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from phone_field import PhoneField
from Attendence import globals
import datetime

year_list   = (('FIRST YEAR', 'FIRST YEAR'), ('SECOND YEAR', 'SECOND YEAR'), ('THIRD YEAR', 'THIRD YEAR'), ('FINAL YEAR', 'FINAL YEAR'),)

branch_list = (('INFORMATION TECHNOLOGY', 'INFORMATION TECHNOLOGY'), ('COMPUTER SCIENCE', 'COMPUTER SCIENCE'), ('ELECTRONIC AND TELECOMMUNICATION ENGINEERING', 'ELECTRONIC AND TELECOMMUNICATION ENGINEERING'), ('MECHANICAL ENGINEERING', 'MECHANICAL ENGINEERING'),('CIVIL ENGINEERING', 'CIVIL ENGINEERING'), ('INSTRUMENTATAL ENGINEERING', 'INSTRUMENTATAL ENGINEERING'),)

subject_list=(('Applied Mathematics', 'Applied Mathematics'), ('Applied Physics', 'Applied Physics'), ('Applied Chemistry', 'Applied Chemistry'),('LD','LD'),('Java','Java'),('PCOM','PCOM'),('MEP','MEP'),('Python','Python'),('IP','IP'),('ADMT','ADMT'),)

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Student(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name="stud_id")
    year        = models.CharField(choices = year_list, max_length=100, default="FIRST YEAR")
    branch      = models.CharField(choices = branch_list, max_length=200, default="INFORMATION TECHNOLOGY")

    def __str__(self):
        return self.user.username

class Subject(models.Model):
    sub_name = models.CharField(choices = subject_list, max_length=100, default="Applied Mathematics")
    year     = models.CharField(choices = year_list, max_length=100, default="FIRST YEAR")
    branch   = models.CharField(choices = branch_list, max_length=100, default="INFORMATION TECHNOLOGY")
    

    
    def __str__(self):
        return self.sub_name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    sub = models.ManyToManyField(Subject,related_name='subjects')
    # sub    = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username



