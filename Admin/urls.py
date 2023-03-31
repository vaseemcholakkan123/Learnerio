from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
import common_views

urlpatterns = [

    path('login/',views.AdminLogin.as_view(),name='adminlogin'),
    path('logout/',LogoutView.as_view(),name='admin_logout'),
    path('remove-admin/<user_id>',views.DemoteAdmin,name='demote_tutor'),


    # #Dashboard view urls
    path('dashboard/',views.AdminPanel.as_view(),name='admin_panel'),
    # path('notification/',views.SendNotification.as_view(),name='send_notification'),
    path('make-admin/<user_id>',views.MakeAdmin,name='make_admin'),
    path('make-admin/<user_id>',views.DemoteAdmin,name='demote_admin'),


    # #User view urls
    path('users/',views.UsersView.as_view(),name='users'),
    path('showprofile/<pk>',common_views.ShowProfile.as_view(),name='showprofile'),
    path('block-user/<user_id>',views.BlockUser,name='block_user'),
    path('unblock-user/<req_id>',views.UnblockUser,name='unblock_user'),

    path('delete-tutorship/<user_id>',views.DemoteTutor,name='demote_tutor'),

    # #Course view urls
    path('courses/',views.CourseView.as_view(),name='courses'),
    path('expanded-course/<course_id>',common_views.CourseDetails.as_view(),name='course_details_admin'),
    path('remove/<course_id>',views.DeleteCourse.as_view(),name='delete_course'),
    # path('/students/<course_id>',views.CourseStudents.as_view(),name='course_students'),

    # #Request view urls
    path('requests/',views.RequestsView.as_view(),name='requests'),
    path('decline/<request_id>',views.DeclineRequest,name='decline_request'),
    path('approve/<request_id>',views.ApproveRequest,name='approve_request'),


    # #Revenue View urls
    path('download-report',views.download_report,name='download_report'),
    path('view-orders',views.OrdersList.as_view(),name='orders'),

    path('add-category',views.add_category,name='add_category'),
    

]