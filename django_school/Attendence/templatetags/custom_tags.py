from django import template
from ..models import Attendence

register = template.Library()

@register.simple_tag
def get_sub_attendence(usr, sub):
    return usr.attendence_set.filter(subject=sub, class_date__range=[globals.date_from, globals.date_to])