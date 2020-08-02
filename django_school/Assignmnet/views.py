from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
# from ..decorators import student_required

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views import generic
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from Assignmnet.models import  Assignment
from classroom.models import *
from Assignmnet.forms import AssignmentForm
# from ..models import  Student, User


class AssgnSubList(TemplateView):
    model=Teacher
    template_name='Assignmnet/sublist.html'

    def get_context_data(self, **kwargs):
        teacher=Teacher.objects.get(user=self.request.user)
        print(teacher)
        subjects=teacher.sub.all()
        # print(subjects)
        # for sub in subjects:
        #     print(sub.sub_name)
        # subjects=Teacher.subjects.all()
        kwargs['sub_list'] = [ sub.sub_name for sub in subjects]
        # print(kwargs['sub_list'])
        return super().get_context_data(**kwargs)


class Assgn(generic.ListView):
    model = Assignment
    template_name = 'Assignmnet/teachassgn.html'

    def get_context_data(self, **kwargs):
        kwargs['assgn'] = Assignment.objects.filter(subject=self.kwargs['sub'])
        kwargs['subject'] = self.kwargs['sub']
        return super().get_context_data(**kwargs)

    # def get(self, request, *args, **kwargs):
    #     kwargs['subject'] = self.kwargs['sub']
    #     print(kwargs)
    #     return super(Assgn,self).get(request, *args, **kwargs)

class StudentAssgn(generic.ListView):
    model = Assignment
    # form_class = TeacherSignUpForm
    template_name = 'Assignmnet/studassgn.html'

    def get_context_data(self, **kwargs):
        # kwargs['user_type'] = 'teacher'
        kwargs['assgn'] = Assignment.objects.all()

        # kwargs['time'] = datetime.now()
        return super().get_context_data(**kwargs)


class AssignmentUpload(generic.CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'Assignmnet/createassgn.html'

    def get_context_data(self, **kwargs):
        kwargs['assgn'] = Assignment.objects.all()
        kwargs['subject'] = self.kwargs['sub']
        print(kwargs['subject'])
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('teachassgn', kwargs={'sub':self.kwargs['sub']})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.subject = self.kwargs['sub']
            obj.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



    
    
# def AssignmentUpload(request,sub):
#     print(sub)
#     if request.method == 'POST':        
#         form = AssignmentForm(request.POST, request.FILES)
#         if form.is_valid():       
#             print("Form valid") 
#             form.save()
#             return redirect('teachassgn' ,sub)
#     else:
#         form = AssignmentForm()
#     return render(request, 'Assignmnet/createassgn.html', {
#         'form': form
#     })

# def edit_item(request, pk, model, cls):
#     item = get_object_or_404(model, pk=pk)

#     if request.method == "POST":
#         form = cls(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = cls(instance=item)

#         return render(request, 'inv/edit_item.html', {'form': form})



def DeleteAssgn(request, pk, sub):
    print(sub)
    Assignment.objects.filter(id=pk).delete()

    return redirect('teachassgn', sub=sub)

