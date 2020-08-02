from django.urls import include, path,re_path

from .views import classroom, students, teachers

urlpatterns = [
    path('', classroom.index, name='home'),
    re_path(r'^about$', classroom.aboutus , name='aboutus'),
    path('students/', students.Studinfo.as_view(),name='studinformation'),
    path('teachers/', teachers.Teachinfo.as_view(),name='teachinformation'),

    path('students/', include(([
        path('dashboard/', students.student, name='student'),
        
    ], 'classroom'), namespace='students')),
    
    path('teachers/', include(([
        path('dashboard/', teachers.teacher, name='teacher'),
        #path('dashboard/subjects/',teachers.Studinfo.as_view(),name='studinfo'),
       
        
    ], 'classroom'), namespace='teachers')),
    ]
