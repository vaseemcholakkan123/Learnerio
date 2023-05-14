from Tutor.models import Course
from django.views.generic import DetailView,ListView

from User.models import User,EnrolledCourse


class CourseDetails(DetailView):

    model = Course
    context_object_name = 'course'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            enrolled_courses = EnrolledCourse.objects.filter(user=request.user)
            current_course = Course.objects.get(id=kwargs['pk'])

            if enrolled_courses is not None:
                for enrolled_course in enrolled_courses:
                    if current_course.title in enrolled_course.course.title:
                        self.extra_context['user_enrolled'] = True
                    else:
                        self.extra_context['user_enrolled'] = False
        else:
            self.extra_context['user_enrolled'] = False          


        return super().get(request, *args, **kwargs)

class ListCourse(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = 'Detail.html'
    def get_queryset(self):
        self.queryset = Course.objects.filter(completed=True)
        return super().get_queryset()




class ShowProfile(DetailView):
    model = User
    template_name = 'Detail.html'
    