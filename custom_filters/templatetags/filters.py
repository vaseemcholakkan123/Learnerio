

from django import template

register = template.Library()

@register.filter
def comma_filter(str):
    if str is None:
        return str
    str = str.split(',')
    if str != '':
        return str
    
from datetime import date as date_x 
from datetime import datetime as time_x

@register.filter
def date_filter(date):
    date =  date_x.today() - date
    return date.days