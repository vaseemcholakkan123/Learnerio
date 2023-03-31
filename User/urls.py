from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView,PasswordChangeView
import common_views

urlpatterns = [    
    path('login/',views.UserLogin.as_view(),name='login'),
    path('create/',views.CreateUser.as_view(),name='create_account'),
    path('verify-email/',views.VerifyEmail.as_view(),name='verify_email'),
  
    path('logout/',LogoutView.as_view(),name='logout'),
    path('become-a-tutor/',views.BecomeTutor.as_view(),name='become_tutor'),
    path('delete/',views.delete_user,name='delete_account'),
    path('dashboard',views.UserDashboard.as_view(),name='user_dashboard'),
    path('change-password/',views.ChangePassword.as_view(),name='change_password'),
    path('edit-profile/<pk>',views.EditProfile.as_view(),name='edit_profile'),
    path('unblock/',views.request_unblock,name='request_unblock'),

    #Wishlist View urls

    path('wishlist/',views.WishlistView.as_view(),name='wishlist'),
    path('to-wishlist/<course>',views.ItemToWishlist,name='add_to_wishlist'),
    path('remove-wishlist-item/<pk>',views.DeleteWishlistItem.as_view(),name='delete_wishlist_item'),
     
    #Cart View urls 

    path('cart/',views.CartView.as_view(),name='cart'),
    path('razorpay-payment',views.razorpay_payment_handler,name='razorpay_payment'),
    path('to-cart/<course>',views.ItemToCart,name='add_to_cart'),
    path('remove-cart-item/<pk>',views.DeleteCartItem.as_view(),name='delete_cart_item'),

    path('my-courses/',views.EnrolledCourseView.as_view(),name='enrolledcourses'),
    path('course-reading/<pk>',views.CourseReading.as_view(),name='continue_reading'),
    path('course-expdanded/<pk>',common_views.CourseDetails.as_view(),name='course_details'),
    path('add-comment/<chapter_id>',views.add_comment,name='add_comment'),
    path('reply-comment/<chapter_id>,<comment_id>',views.reply_comment,name='reply_comment'),
    path('add-review/<course_id>',views.add_review,name='add_review'),
    path('delete-review/<review_id>,<course_id>',views.delete_review,name='delete_review'),
    path('download-certificate/<course_id>',views.download_certificate,name='download_certificate'),




]