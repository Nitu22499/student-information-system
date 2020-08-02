from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:teacher')
        else:
            return redirect('students:student')
    return render(request,'classroom/index.html',{})

def aboutus(request):
    return render(request,'classroom/aboutus.html',{})
