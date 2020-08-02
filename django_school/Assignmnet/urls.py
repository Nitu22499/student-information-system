from django.urls import include, path,re_path

from classroom.views import classroom, students, teachers
from . import views

 
urlpatterns = [
    path('teachers/dashboard/teach_sublist/', views.AssgnSubList.as_view(), name='teach_sublist'),
    path('teachers/dashboard/teachassgn/<str:sub>', views.Assgn.as_view(), name='teachassgn'),
    path('students/dashboard/studentassgn/', views.StudentAssgn.as_view(), name='studentassgn'),
    path('teachers/dashboard/addassignment/<str:sub>', views.AssignmentUpload.as_view(), name='assgnform'),
    # re_path(r'^assgn/delete/(?P<pk>\d+)$',views.DeleteAssgn, name="delete_assgn"),
    path('teachers/dashboard/delete_assgn/<int:pk>/<str:sub>', views.DeleteAssgn, name="delete_assgn")
    
]