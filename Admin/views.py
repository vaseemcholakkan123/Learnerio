from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView,ListView,DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from Tutor.models import Course
from User.models import User
from Tutor.models import Tutor,Categories
from .models import Request,Orders
from django.shortcuts import redirect
from django.db.models import Sum
from django.http import HttpResponse
import csv
from datetime import date


class AdminLogin(LoginView):
    template_name = 'Admin/Login.html'
    success_url = '/admin/dashboard'

    def get_success_url(self) -> str:
        return self.success_url

class AdminPanel(TemplateView,PermissionRequiredMixin):

    def get(self, request, *args, **kwargs):
        
        bill_sum = Orders.objects.aggregate(Sum('bill_amount'))
        self.extra_context = {'bill_amount':bill_sum['bill_amount__sum'],'title':'Dashboard'}

        return super().get(request, *args, **kwargs)
    
    permission_required = 'is_superuser'
    template_name = 'Admin/Dashboard.html'

class UsersView(ListView):
    model = User
    context_object_name = 'users'
    extra_context = {'title':'Users'}
    template_name = 'Admin/User-List.html'

    def post(self,request,*args,**kwargs):
        name = request.POST.get('query')
        tutor = request.POST.get('category')
        if tutor == 'tutor':
            users = User.objects.filter(username__contains=name,is_tutor = True)
        else:
            users = User.objects.filter(username__contains=name)
        
        extra_context = self.extra_context.copy()
        extra_context['users']=users
        self.extra_context = extra_context
        return self.get(request)
    
class CourseView(ListView):
    model = Course
    context_object_name = 'courses'
    extra_context = {'title':'Courses'}
    template_name = 'Admin/Course-List.html'

    def post(self,request,*args,**kwargs):
        name = request.POST.get('query')
        skills = request.POST.get('category')
        
        courses = Course.objects.filter(title__icontains=name,skills_offering__Title__icontains=skills)
        extra_context = self.extra_context.copy()
        extra_context['courses']=courses
        self.extra_context = extra_context
        return self.get(request)

class DeleteCourse(DeleteView):
    model = Course
    success_url = '/admin/dashboard'
    def get(self,request,*args,**kwargs):
        self.post(request,args,kwargs)

class RequestsView(ListView):
    model = Request
    context_object_name = 'Requests'
    template_name = 'Admin/Request-List.html'



def DeclineRequest(request,request_id):
    req = Request.objects.get(id = request_id)
    user = User.objects.get(id=req.user.id)
    user.is_tutor = False
    user.save()
    Tutor.objects.get(user_id=user).delete()
    req.delete()
    return redirect('/admin/requests')

def ApproveRequest(request,request_id):
    req = Request.objects.get(id = request_id)
    user = User.objects.get(id=req.user.id)
    user.is_tutor = True
    user.save()
    req.delete()
    return redirect('/admin/requests')

def BlockUser(request,user_id):
    user = User.objects.get(id=user_id)
    user.is_blocked = True
    user.save()
    return redirect('/admin/users') 

def UnblockUser(request,req_id):
    req = Request.objects.get(id = req_id)
    user = User.objects.get(id=req.user.id)
    user.is_blocked = False
    user.save()
    req.delete()
    return redirect('/admin/users')

def DemoteTutor(request,user_id):
    user = User.objects.get(id=user_id)
    user.is_tutor = False
    user.save()
    return redirect('/admin/users')

def MakeAdmin(request,user_id):
    user = User.objects.get(id=user_id)
    user.is_superuser = True
    user.save()
    return redirect('/admin/users')

def DemoteAdmin(request,user_id):
    user = User.objects.get(id=user_id)
    user.is_superuser = False
    user.save()
    return redirect('/')

class OrdersList(ListView):
    model = Orders
    template_name = 'Admin/Orders.html'
    context_object_name = 'orders'

def download_report(request):
    orders = Orders.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment;filename = "Order Report {date.today()}.csv"'

    csv_writer = csv.writer(response)
    csv_writer.writerow(['order id','courses','user','profit'])

    for order in orders:
        csv_writer.writerow([order.order_id,order.order_course,order.user,order.bill_amount])

    return response

def add_category(request):
    Categories.objects.create(name=request.POST.get('category'))
    return redirect('/admin/dashboard')