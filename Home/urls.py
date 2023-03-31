from . import views
from django.urls import path

urlpatterns = [
    path('',views.HomePage.as_view(),name='home'),
    path('course-details/<pk>',views.ExpandedCourse.as_view(),name='course_details'),
    path('filter',views.filter_ajax,name='filter')
    
    
]