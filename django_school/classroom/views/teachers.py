from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,TemplateView,
                                  UpdateView)

from ..decorators import teacher_required
from ..forms import  TeacherSignUpForm
from ..models import  User,Student,Teacher
from datetime import datetime

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        print(kwargs)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # sub= form.cleaned_data.get("sub")
        # print(sub)
        return redirect('teachers:teacher')

def teacher(request):
    return render(request,"classroom/teachers/teacher.html",{})

class Teachinfo(TemplateView):
    # model = User
    # form_class = TeacherSignUpForm
    template_name = 'classroom/teachers/teachinformation.html'

    def get_context_data(self, **kwargs):
        # kwargs['user_type'] = 'teacher'
        kwargs['teach_list'] = Teacher.objects.all()
        # kwargs['time'] = datetime.now()
        return super().get_context_data(**kwargs)
