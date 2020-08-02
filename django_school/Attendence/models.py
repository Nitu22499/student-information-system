from django.db import models
from django.utils import timezone
from classroom.models import User,Student,Teacher,Subject

subject_list=(('IP', 'IP'), ('IOT', 'IOT'), ('CNS', 'CNS'), ('MEP', 'MEP'), ('ADMT','ADMT'),('BCE','BCE'))

class Attendence(models.Model):

    subject = models.CharField(max_length = 250)
    # subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_date=models.DateTimeField(default=timezone.now)
    # teacher= models.ForeignKey(Teacher,on_delete=models.CASCADE, related_name='class_mentor')
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student)

    
    class Meta:
        ordering = ['subject', 'class_date']
    

 
 