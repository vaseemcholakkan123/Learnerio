from django.db import models
from django.contrib.auth.models import AbstractUser


#custom user

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics',null=True)
    date_of_birth = models.DateField(null=True)
    is_tutor = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    

class Wishlist(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    course_id = models.ForeignKey('Tutor.Course',related_name='wishlist_courses',on_delete=models.CASCADE,null=True)

class Cart(models.Model):
    user_id = models.ForeignKey(User,related_name='user_cart',on_delete=models.CASCADE)
    course_id = models.ForeignKey('Tutor.course',related_name='cart_courses',on_delete=models.CASCADE,null=True)


class EnrolledCourse(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey('Tutor.course',on_delete=models.DO_NOTHING)

class Read_Chapter(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    chapter = models.ForeignKey('Tutor.chapters',related_name='read_chapters',on_delete=models.CASCADE)

