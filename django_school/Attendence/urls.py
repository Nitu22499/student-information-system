from django.urls import include, path,re_path

# from classroom.views import classroom, students, teachers
from Attendence.views import AttendenceView,SubList,RecordAttendence,SubmitAttendence
 
urlpatterns = [
    path('teachers/dashboard/attendence', AttendenceView.as_view(), name='attendence'),
    path('students/dashboard/attendence', AttendenceView.as_view(), name='attendence'),
    path('teachers/dashboard/record_attendence/<str:sub>', RecordAttendence.as_view(), name='record_attendence'),
    path('teachers/dashboard/subject',SubList.as_view(), name='subject'),
    path('teachers/dashboard/submit_attend/<str:sub>',SubmitAttendence, name='submit'),


]