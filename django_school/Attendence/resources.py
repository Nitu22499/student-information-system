from import_export import resources
from .models import Attendence

class AttendenceResource(resources.ModelResource):
    class Meta:
        model =Attendence