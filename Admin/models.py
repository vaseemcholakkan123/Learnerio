from django.db import models
from User.models import User
from Tutor.models import Course



class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)

class Request(models.Model):
    description = models.CharField(max_length=100,null=False)
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)

class Orders(models.Model):
    order_id = models.CharField(max_length=100,null=False)
    order_course = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    bill_amount = models.FloatField(null=False,default=0)



