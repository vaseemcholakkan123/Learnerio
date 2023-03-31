from django.db import models
from User.models import User

QUALIFICATION = (('Degree','Degree'),
                 ('Msc Computer Science','Msc Computer Science'),
                 ('Bsc Computer Science','Bsc Computer Science'),
                 ('MBA','MBA'),
                 ('BBA','BBA'),
                 ('Bsc Biology','Bsc Biology'),
                 ('Self Studied','Self Studied'))

LEVELS = (('Beginner','Beginner'),
          ("Intermediate",'Intermediate'),
          ('Advanced','Advanced'),
          ('Mixed','Mixed'))

LANGUAGE = (('English','English'),
          ("Malayalam",'Malayalam'),
          ('Hindi','Hindi'),)

DURATION = ((1,'1 month'),
            (2,'2 months'),
            (3,'3 months'),
            (4,'4 months'),
            (5,'5 months'),
            (6,'6 months'),
            (7,'7 months'),
            (8,'8 months'),
            (9,'9 months'),)

CHAPTERS = (
            (2,'2 chapters'),
            (3,'3 chapters'),
            (4,'4 chapters'),
            (5,'5 chapters'),
            (6,'6 chapters'),
            (7,'7 chapters'),
            (8,'8 chapters'),
            (9,'9 chapters'),
            (10,'10 chapters'),)

# CATEGORIES = (
#             ('It & Software','It & Software'),
#             ('Business & Finance','Business & Finance'),
#             ('Health','Health & Fitness'),
#             ('Marketing','Marketing'),
#             )

class Categories(models.Model):
    name = models.CharField(max_length=150,unique=True)

    def __str__(self):
        return self.name

class Skills(models.Model):
    category = models.ManyToManyField(Categories)
    Title = models.CharField(max_length=100)

    class Meta():
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
    def __str__(self):
        return self.Title
    

        
class Tutor(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    qualification = models.CharField(choices=QUALIFICATION,null=False,max_length=100)
    skills = models.ManyToManyField(Skills)
    mobile = models.CharField(max_length=10,null=False,blank=True)
    class Meta():
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutors'
    def __str__(self):
        return self.user_id.username




class Course(models.Model):
    owner = models.ForeignKey(Tutor,related_name='tutor_course',on_delete=models.CASCADE)
    title = models.CharField(max_length=150,null=False)
    description = models.TextField(null=False,max_length=200)
    overview = models.TextField(null=False)
    whats_learning = models.TextField(null=False)
    requirements = models.TextField(null=False)
    image = models.ImageField(upload_to='CourseImages',null=False)
    updated_date = models.DateField(auto_now=True)
    preview = models.FileField(upload_to='course_previews')
    duration = models.IntegerField(choices=DURATION,null=False)
    related_topics = models.ManyToManyField(Skills)
    category = models.ManyToManyField(Categories)
    chapters = models.IntegerField(choices=CHAPTERS,null=True)
    level = models.CharField(choices=LEVELS,null=False,max_length=100)
    price = models.FloatField(null=False)
    rating = models.BigIntegerField(null=False,default=0)
    completed = models.BooleanField(default=False)
    students_enrolled = models.IntegerField(default=0)

    def __str__(self):
        return self.title



class Review(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    rating = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    review_text = models.TextField(null=False,blank=True)
    posted_date = models.DateField(auto_now_add=True)

    
class Chapters(models.Model):
    course = models.ForeignKey(Course,related_name='course_chapters',on_delete=models.CASCADE)
    chapter_no = models.IntegerField(default=1)
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='Chapters')
    description = models.TextField()


class Comment(models.Model):
    chapter = models.ForeignKey(Chapters,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length=150)
    reply_comment = models.ForeignKey('self',related_name='comment_reply',on_delete=models.SET_NULL,null=True,blank=True)
    posted_date = models.DateField(auto_now_add=True)
