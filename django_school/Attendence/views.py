from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from classroom.decorators import teacher_required
from django.views.generic import TemplateView
from django.views import generic
from Attendence.forms import AttendenceForm
from Attendence.models import  Attendence
from classroom.models import  User,Student,Teacher,Subject
from datetime import datetime, date
# import datetime
from Attendence.models import subject_list
from . import globals
from math import ceil
from collections import OrderedDict


# Create your views here.
class AttendenceView(ListView):
    model = User
    # form_class = AttendenceForm
    template_name = 'attendence/report.html'
    context_object_name="studlist"
    subject_list=[]

    subject = '-'

    def get(self, request, *args, **kwargs):
        self.subject_list= []
        if self.request.GET.get('date_from'):
            temp_date_from = datetime.strptime(self.request.GET.get('date_from'), "%d/%m/%Y").date()               
            globals.date_from = datetime(temp_date_from.year, temp_date_from.month, temp_date_from.day)
        else:
            globals.date_from = datetime(2019, 1, 1)
        if self.request.GET.get('date_to'):
            temp_date_to = datetime.strptime(self.request.GET.get('date_to'), "%d/%m/%Y").date()   
            globals.date_to = datetime(temp_date_to.year, temp_date_to.month, temp_date_to.day, 23, 59, 59)
        else:
            date_to = datetime.now()
        self.subject = self.request.GET.get('input_subject')   
        
        # print(Attendence.get_Python.all())
        return super(AttendenceView, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if globals.date_from == datetime(2019, 1, 1):
            kwargs['date_from'] = '-'
        else:
            kwargs['date_from'] = globals.date_from
        kwargs['date_to'] = globals.date_to
        kwargs['subject'] = self.subject

        
        # print("kwargs", globals.date_from, globals.date_to)

        table_head = OrderedDict()
        table_body = OrderedDict()
        table_percentage = OrderedDict()
        total = 0
        present = 0
        percent = 0

        #subject list for student
        if self.request.user.is_student:
            student=Student.objects.get(user=self.request.user)
            stud_year = student.year
            stud_branch = student.branch
            for subject in Subject.objects.filter(year=stud_year, branch=stud_branch):
                if subject.sub_name not in self.subject_list:
                    self.subject_list.append(subject.sub_name)

        # subject list for teacher
        else:
            teacher=Teacher.objects.get(user=self.request.user)
            subjects=teacher.sub.all()
            
            for subject in subjects:
                if subject.sub_name not in self.subject_list:
                    self.subject_list.append(subject.sub_name)     

        kwargs['subject_list'] = self.subject_list
        # print(self.subject_list)
        

        # for all subjects
        if self.subject == 'Select Subject':                      

            # creating the table header. Retreiving subjects and dates as required to show in the table header.
            if self.request.user.is_student:
                qset = self.request.user.attendence_set.filter(class_date__range=[globals.date_from, globals.date_to])
            else:
                qset = Attendence.objects.filter(subject__in=self.subject_list,class_date__range=[globals.date_from, globals.date_to])
            # print(qset)
            for obj in qset:
                if obj.subject in table_head.keys():
                    if obj.class_date not in table_head[obj.subject]:
                        table_head[obj.subject].append(obj.class_date)
                else:
                    table_head[obj.subject] = [obj.class_date, ]

            # print(table_head)

            for obj in qset:
                student_name = obj.student.first_name + " " + obj.student.last_name
                if student_name in table_body.keys():
                    if obj.subject in table_body[student_name].keys():
                        table_body[student_name][obj.subject].append({obj.class_date:obj.is_present})
                    else:
                        table_body[student_name][obj.subject] = [{obj.class_date:obj.is_present}, ]
                else:
                    table_body[student_name] = {obj.subject:[{obj.class_date:obj.is_present},],}


                if student_name in table_percentage.keys():
                    if obj.subject in table_percentage[student_name].keys():
                        table_percentage[student_name][obj.subject] = 0
                    else:
                        table_percentage[student_name][obj.subject] = 0
                else:
                    table_percentage[student_name] = {obj.subject:0}

            # print(table_body)
            
            

            # calclating attendence percentage subjec wise.
            
            for subject in self.subject_list:
                subject_var = Subject.objects.get(sub_name=subject)
                year = subject_var.year
                branch = subject_var.branch
        
                students = User.objects.filter(stud_id__year = year, stud_id__branch = branch)
                for usr in students:
                    # print(usr)
                    total = Attendence.objects.filter(student=usr, subject=subject).count()
                    # print(total)
                    present = Attendence.objects.filter(student=usr, subject=subject, is_present=True).count()
                    # print(present)
                    if total != 0:
                        percent = (present * 100) / total
                    else:
                        percent = 0

                    try:
                        table_percentage[usr.first_name + " " + usr.last_name][subject] = ceil(percent)
                    except:
                        pass

            

        # when only particular subject is selected.   
        else:
            if self.request.user.is_student:       
                qset = self.request.user.attendence_set.filter(subject=self.subject, class_date__range=[globals.date_from, globals.date_to])
            else:
                qset=Attendence.objects.filter(subject=self.subject, class_date__range=[globals.date_from, globals.date_to])
            # print(qset)
            for obj in qset:
                if obj.subject in table_head.keys():
                    if obj.class_date not in table_head[obj.subject]:
                        table_head[obj.subject].append(obj.class_date)
                else:
                    table_head[obj.subject] = [obj.class_date, ]

            for obj in qset:
                student_name = obj.student.first_name + " " + obj.student.last_name
                if student_name in table_body.keys():
                    if obj.subject in table_body[student_name].keys():
                        table_body[student_name][obj.subject].append({obj.class_date:obj.is_present})
                    else:
                        table_body[student_name][obj.subject] = [{obj.class_date:obj.is_present}, ]
                else:
                    table_body[student_name] = {obj.subject:[{obj.class_date:obj.is_present},],}


                if student_name in table_percentage.keys():
                    if obj.subject in table_percentage[student_name].keys():
                        table_percentage[student_name][obj.subject] = 0
                    else:
                        table_percentage[student_name][obj.subject] = 0
                else:
                    table_percentage[student_name] = {obj.subject:0}

            # print(table_body)
            
            

            for subject in self.subject_list:
                subject_var = Subject.objects.get(sub_name=subject)
                year = subject_var.year
                branch = subject_var.branch
        
                students = User.objects.filter(stud_id__year = year, stud_id__branch = branch)
                for usr in students:
                    # print(usr)
                    total = Attendence.objects.filter(student=usr, subject=subject).count()
                    # print(total)
                    present = Attendence.objects.filter(student=usr, subject=subject, is_present=True).count()
                    # print(present)
                    if total != 0:
                        percent = (present * 100) / total
                    else:
                        percent = 0

                    try:
                        table_percentage[usr.first_name + " " + usr.last_name][subject] = ceil(percent)
                    except:
                        pass            
            
        kwargs['table_head'] = table_head
        kwargs['table_body'] = table_body
        kwargs['table_percentage'] = table_percentage

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        # return User.objects.filter(is_student = True)
        if self.subject == 'Select Subject':
            if self.request.user.is_student:
                return User.objects.filter(id = self.request.user.id, attendence__class_date__range=[globals.date_from, globals.date_to]).distinct()
            else:
                return User.objects.filter(is_student = True, attendence__class_date__range=[globals.date_from, globals.date_to]).distinct()

        else:
            if self.request.user.is_student:
                return User.objects.filter(id = self.request.user.id, attendence__class_date__range=[globals.date_from, globals.date_to], attendence__subject = self.subject).distinct()
            else:
                return User.objects.filter(is_student = True, attendence__class_date__range=[globals.date_from, globals.date_to], attendence__subject = self.subject).distinct()
            

class RecordAttendence(ListView):
    model = User
    template_name = 'attendence/stud_info.html'
    context_object_name="stud"

    def get_queryset(self):
        subject = Subject.objects.get(sub_name=self.kwargs['sub'])
        year = subject.year
        branch=subject.branch
        
        students = User.objects.filter(stud_id__year = year, stud_id__branch = branch)
        # print(students)

        return students

    def get_context_data(self, **kwargs):
        kwargs['date'] = datetime.now()
        kwargs['subject'] = self.kwargs['sub']
        # print(kwargs['subject'])
        return super().get_context_data(**kwargs)


class SubList(TemplateView):
    model=Teacher
    template_name='attendence/sub_list.html'

    def get_context_data(self, **kwargs):
        teacher=Teacher.objects.get(user=self.request.user)
        # print(teacher)
        subjects=teacher.sub.all()        
        kwargs['sub_list'] = [ sub.sub_name for sub in subjects]
        # print(kwargs['sub_list'])
        return super().get_context_data(**kwargs)

def SubmitAttendence(request, sub):
    is_present_list = request.POST.getlist('checks[]')
    
    subject = Subject.objects.get(sub_name=sub)
    year = subject.year
    branch=subject.branch
    all_students = User.objects.filter(stud_id__year = year, stud_id__branch = branch)
    current_date = datetime.now()
    for student in all_students:
        # print(student.id)
        obj = Attendence()
        obj.student = student
        obj.subject = sub
        if str(student.id) in is_present_list:
            # print("Match")
            obj.is_present = True  
        obj.class_date = current_date      
        obj.save()
        # is_present = False
        globals.date_to = datetime.now()
    return redirect('subject')
    
    