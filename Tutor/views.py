from django.views.generic import CreateView,UpdateView,DeleteView,TemplateView,ListView
from .models import Course,Chapters,Categories
from Tutor.models import Tutor,Skills
from django.shortcuts import redirect,render
from .forms import CourseForm
from User.forms import BecomeTutor
from django.forms import modelformset_factory
from Tutor.models import Categories
from Admin.models import Orders
from django.http import HttpResponse
import csv 
from datetime import date

# Create your views here.

# function to get tutor id
def get_tutor_id(userObject):
    tutor = Tutor.objects.get(user_id=userObject.id)
    return tutor.id


class PostCourse(CreateView):
    model = Course
    form_class = CourseForm
    success_url = '/Tutor/dashboard'
    template_name = 'Tutor/Post-Course.html'

    extra_context = {'title':'Post Course','categories':Categories.objects.all()}

    def form_valid(self, form: CourseForm):
        req_csv = ''
        learns_csv = ''
        for reqs in self.request.POST.getlist('requirements'):
            req_csv += reqs + ','

        for learns in self.request.POST.getlist('learns'):
            learns_csv += learns + ','

        try:
            current_tutor = Tutor.objects.get(user_id=self.request.user)
            form.instance.owner = current_tutor
            form.instance.whats_learning = learns_csv
            form.instance.requirements = req_csv
            form.instance.save()
            form.instance.category.add(form.cleaned_data.get('category'))
            form.instance.save()
            
        except Tutor.DoesNotExist:
            form.add_error(None,'You are not tutor')
        
        return redirect('/Tutor/add-chapters'+f'?course_id={form.instance.id}')
        
        
    
def add_chapters(request):

    course_id = request.GET.get('course_id')
    try:
        course = Course.objects.get(id=course_id)
    except:
        raise ValueError('Something wrong !')
    
    chapters_count = course.chapters

    formset_class = modelformset_factory(Chapters,extra=chapters_count,exclude=['course'])

    form = formset_class(queryset=Chapters.objects.none())

    if request.method == 'POST':
        
        forms = formset_class(request.POST,request.FILES)

        for form in forms:
            print(form.errors,'lklklklllkl')
            form.instance.course = course
            form.save() 
        course.completed = True
        course.save()
        return redirect('/Tutor/posted-courses')

    return render(request,template_name='Tutor/Post-Chapters.html',context={'form_set':form,'title':'Add Chapters'})


def edit_chapters(request):
    
    course_id = request.GET.get('course_id')
    try:
        course = Course.objects.get(id=course_id)
    except:
        raise ValueError('Something wrong !')

    formset_class = modelformset_factory(Chapters,extra=4,exclude=['course'])

    form = formset_class(queryset=Chapters.objects.filter(course=course))

    if request.method == 'POST':

        forms = formset_class(request.POST,request.FILES,queryset=Chapters.objects.filter(course=course))
        

        if forms.is_valid():
            print(forms.errors,';/;/;/;/')
            forms.save()
        else:
            print(forms.errors,';/;/;/;/','\non else')
            return render(request,template_name='Tutor/Post-Chapters.html',context={'form_set':form,'title':'Edit Chapters'})


        return redirect('/Tutor/posted-courses')

    return render(request,template_name='Tutor/Post-Chapters.html',context={'form_set':form,'title':'Edit Chapters'})
 


class EditCourse(UpdateView):
    model = Course
    form_class = CourseForm
    extra_context = {'update':True}
    success_url = '/Tutor/posted-courses'
    template_name = 'Tutor/Post-Course.html'

    def form_valid(self, form: CourseForm):
        req_csv = ''
        learns_csv = ''
        for reqs in self.request.POST.getlist('requirements'):
            req_csv += reqs + ','

        for learns in self.request.POST.getlist('learns'):
            learns_csv += learns + ','

        try:
            current_tutor = Tutor.objects.get(user_id=self.request.user)
            form.instance.owner = current_tutor
            form.instance.whats_learning = learns_csv
            form.instance.requirements = req_csv
            form.instance.category.add(form.cleaned_data.get('category'))
            form.instance.save()
        except Tutor.DoesNotExist:
            form.add_error(None,'You are not tutor')

        
        
        return redirect('/Tutor/edit-chapters'+f'?course_id={form.instance.id}')

class DeleteCourse(DeleteView):
    model = Course
    success_url = '/Tutor/posted-courses'

    def get(self, request,*args, **kwargs):
        return self.post(request, *args, **kwargs)
    
class TutorDashboard(TemplateView):
    
    template_name = 'Tutor/Dashboard.html'

    def get(self, request, *args, **kwargs):
        tutor_id = get_tutor_id(request.user)
        self.extra_context = {'title':'Tutor Panel','tutor_id':tutor_id}
        return super().get(request, *args, **kwargs)

class TutorCourses(TemplateView):
     template_name = 'Tutor/Tutor-Courses.html'

     def get(self, request, *args,**kwargs):
        tutor_id = get_tutor_id(request.user)
        self.extra_context = {'courses':Course.objects.filter(owner=tutor_id)} 
        return super().get(request, *args, **kwargs)
    
class EditTutorProfile(UpdateView):
    model = Tutor
    form_class = BecomeTutor
    extra_context = {'update':True}
    success_url = '/Tutor/dashboard'
    template_name = 'User/Tutor-Form.html'

    def form_valid(self, form: CourseForm):
        form.instance.user_ids = self.request.user
        return super().form_valid(form)


    
def exit_tutor(request):
    request.user.is_tutor = False
    request.user.save()
    return redirect('/')

     
def add_skill(request):
    try:
        print(request.POST.get('category'),';/;/;/;///')
        category_data = Categories.objects.get(id = request.POST.get('category'))
    except:
        print('error')

    new_skill = Skills.objects.create(Title=request.POST.get('skill'))
    new_skill.category.add(category_data)
    x = new_skill.save()
    return redirect('become_tutor')
    
class TutorProfits(ListView):
    model = Orders
    template_name = 'Tutor/Orders.html'
    context_object_name = 'orders'

    def get(self, request, *args, **kwargs):
        tutor = Tutor.objects.get(id=kwargs['pk'])
        self.extra_context = {'tutor_id':kwargs['pk']}
        self.queryset = Orders.objects.filter(order_course__owner=tutor)
        return super().get(request, *args, **kwargs)


def download_report(request,tutor_id):
    tutor = Tutor.objects.get(id=tutor_id)
    orders = Orders.objects.filter(order_course__owner=tutor)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment;filename = "Order Report {date.today()}.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerow(['order id','courses','user','profit'])

    for order in orders:
        csv_writer.writerow([order.order_id,order.order_course,order.user,order.order_course.price])

    return response