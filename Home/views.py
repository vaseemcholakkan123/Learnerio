from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from Tutor.models import Course 
from common_views import ListCourse,CourseDetails
from Tutor.models import Categories
from django.db import models
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import render_to_string
import json
from Tutor.models import Tutor
import os
from django.conf import settings

# Create your views here.

class HomePage(ListCourse):

    template_name = 'Home/HomePage.html'

    def get(self, request, *args, **kwargs):
        try:
            category = Categories.objects.all()
        except:
            category = None

        self.extra_context = {'title':'Learner.io','categories':category}

        print(request.GET,'\n\n\ndffdd\n\n\n')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = Course.objects.all().annotate(avg_rating = models.Avg('review__rating'))
        search = self.extra_context.get('searchname')
       
        if search:
            self.queryset = Course.objects.filter(title__icontains=search)
        
        return self.queryset
    
    def post(self,request,*args,**kwargs):
        name = request.POST.get('query')

        extra_context = {'searchname':name}

        self.extra_context = extra_context
        
        return super().get(request)
    
class ExpandedCourse(CourseDetails):
    extra_context = {'title':'Course Details'}
    template_name = 'Home/Course-View.html'





def filter_ajax(request):
     
    filter_by_skill = request.GET.get('filter-by-category')
    filter_by_level = request.GET.get('filter-by-level')
    filter_by = request.GET.get('filter-by')
    
    if filter_by_skill:
        print('setting queryset')
        courses = Course.objects.filter(category__name__icontains = filter_by_skill)

    if filter_by:
        if filter_by == 'price':
            courses = Course.objects.all().order_by('price')
        else:
            courses = Course.objects.all().order_by('rating')

    if filter_by_level:
        courses = Course.objects.filter(level__icontains = filter_by_level)

    serialized_courses = serializers.serialize('json', courses)

    courses_list = []
    for course in json.loads(serialized_courses):

        course_dict = {
            'id': Course.objects.get(title=course.get('fields').get('title')).id,
            'name': course.get('fields').get('title'),
            'description': course.get('fields').get('description'),
            'price': course.get('fields').get('price'),
            'rating': course.get('fields').get('rating'),
            'category':Categories.objects.get(id=course.get('fields').get('category')[0]).name,
            'updated_date': course.get('fields').get('updated_date'),
            'tutor': Tutor.objects.get(id=course.get('fields').get('owner')).user_id.username,
            'tutor_profile':str(Tutor.objects.get(id=course.get('fields').get('owner')).user_id.profile_pic),
            'course_img':str(course.get('fields').get('image')),
            'level': course.get('fields').get('level'),
            'duration': course.get('fields').get('duration'),
        }

        courses_list.append(course_dict)

    return JsonResponse(courses_list, safe=False)
