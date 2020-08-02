from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import  Student,Teacher, User , Subject


class TeacherSignUpForm(UserCreationForm):
    # subject_list=(('Applied Mathematics', 'Applied Mathematics'), ('Applied Physics', 'Applied Physics'), ('Applied Chemistry', 'Applied Chemistry'),('LD','LD'),('Java','Java'),('PCOM','PCOM'),('MEP','MEP'),('Python','Python'),)

    sub = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),widget=forms.CheckboxSelectMultiple, required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields=('username','first_name','last_name','email',)

    def save(self, commit=True):
        # data=self.cleaned_data
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()

        teacher = Teacher.objects.create(user=user)
        # teacher = Teacher(user=user,sub=data['sub'],)
        teacher.sub.add(*self.cleaned_data.get('sub'))
        # teacher.save()
        return user
    
class StudentSignUpForm(UserCreationForm):
   year_list=(('FIRST YEAR', 'FIRST YEAR'), ('SECOND YEAR', 'SECOND YEAR'), ('THIRD YEAR', 'THIRD YEAR'), ('FINAL YEAR', 'FINAL YEAR'),)
   branch_list=(('INFORMATION TECHNOLOGY', 'INFORMATION TECHNOLOGY'), ('COMPUTER SCIENCE', 'COMPUTER SCIENCE'), ('ELECTRONIC AND TELECOMMUNICATION ENGINEERING', 'ELECTRONIC AND TELECOMMUNICATION ENGINEERING'), ('MECHANICAL ENGINEERING', 'MECHANICAL ENGINEERING'),('CIVIL ENGINEERING', 'CIVIL ENGINEERING'), ('INSTRUMENTATAL ENGINEERING', 'INSTRUMENTATAL ENGINEERING'),)
   
   year = forms.CharField(widget=forms.Select(choices=year_list),required=True)
   branch = forms.CharField(widget=forms.Select(choices=branch_list),required=True)

   class Meta(UserCreationForm.Meta):
        model = User
        fields=('username','first_name','last_name','email',)

#    class Meta(UserCreationForm.Meta):
#         model = Student
#         fields=('user.username','user.first_name','user.last_name','user.email','year',)

   @transaction.atomic
   def save(self):
        data=self.cleaned_data
        # user = User(email=data['email'],first_name=data['first_name'],last_name=data['last_name'])
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student = Student(user=user,year=data['year'], branch=data['branch'])
         
        # student.year.add(*self.cleaned_data.get('year'))
        # student.branch.add(*self.cleaned_data.get('branch'))
        student.save()
        return user

