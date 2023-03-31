import common_views
from django.urls import path
from . import views
urlpatterns = [

    # # Dashboard and urls
    path('dashboard/',views.TutorDashboard.as_view(),name='tutor_dashboard'),
    path('edit-tutor-profile/<pk>',views.EditTutorProfile.as_view(),name='edit_tutor_profile'),
    path('tutor-profit/<pk>',views.TutorProfits.as_view(),name='tutor_profits'),
    path('exit-tutorship',views.exit_tutor,name='exit_tutorship'),
    
    # # Post Course urls
    path('post-course',views.PostCourse.as_view(),name='post_course'),
    path('add-skill',views.add_skill,name='add_skill'),
    path('posted-courses',views.TutorCourses.as_view(),name='tutor_courses'),
    path('add-chapters',views.add_chapters,name='add_chapters'),
    path('edit-chapters',views.edit_chapters,name='edit_chapters'),
    path('edit-course/<pk>',views.EditCourse.as_view(),name='edit_course'),
    path('delete-course/<pk>',views.DeleteCourse.as_view(),name='delete_course'),
    path('download-report/<tutor_id>',views.download_report,name='download_report_tutor'),
    
]