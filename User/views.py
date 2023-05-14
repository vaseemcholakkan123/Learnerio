from django.contrib.auth.views import *
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserCreationForm,UserUpdateForm
from .models import *
from Tutor.models import * 
from Admin.models import Request,Orders
from django.shortcuts import redirect,HttpResponse
from verify_email.email_handler import send_verification_email
from .forms import LoginForm,BecomeTutor
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.http import FileResponse
import os
from django.http import HttpResponse
from pathlib import Path
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.

class UserLogin(LoginView):
    success_url = 'home'
    form_class = LoginForm
    template_name = 'User/Login.html'
    

class CreateUser(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = '/user/login'
    extra_context = {'title':'Create'}
    template_name = 'User/CreateAccount.html'

    def form_valid(self, form):
        send_verification_email(self.request,form)
        return redirect('/user/verify-email')
    
    
class VerifyEmail(TemplateView):
    template_name = 'User/Verify-Email.html'
    extra_context = {'title':'Verify Email'}

class EditProfile(UpdateView,LoginRequiredMixin):
    model = User
    success_url = '/user/dashboard'
    form_class = UserUpdateForm
    template_name = 'User/Edit-Profile.html'

def delete_user(request):
    request.user.is_blocked = True
    request.user.save()
    logout(request)
    return redirect('/user/login')
    
class ChangePassword(PasswordChangeView,LoginRequiredMixin):
    success_url = '/user/dashboard'
    template_name = 'User/Password-Change.html'
    
    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data.get('new_password1'))
        self.request.user.save()
        update_session_auth_hash(self.request, self.request.user)
        return redirect(self.success_url)
    
def request_unblock(request):
    try:
        username = request.POST['username']
        user = User.objects.get(username=username)
       
    except:
        print('try worked excepted')
        user = None
        
    Request.objects.create(user=user,description='unblock')
    return redirect('/user/login')


class UserDashboard(TemplateView,LoginRequiredMixin):
    extra_context = {'title':'User Dashboard'}
    template_name = 'User/Dashboard.html'

    
class BecomeTutor(CreateView,LoginRequiredMixin):
    model = Tutor
    form_class = BecomeTutor
    success_url = '/'
    template_name = 'User/Tutor-Form.html'
    extra_context = {'title':'Become Tutor','categories':Categories.objects.all()}


    def form_valid(self, form):
        form.instance.user_id = self.request.user
        print('form instance \n\n\n\n',form.cleaned_data)

        request = Request.objects.create(user = self.request.user,description= 'become tutor')
        request.save()
        if Tutor.objects.filter(user_id=request.user).exists():
            return redirect('/')
        return super().form_valid(form)
    
# Wishlist views

class WishlistView(TemplateView,LoginRequiredMixin):
    template_name = 'User/Wishlist.html'

    def get(self, request, *args, **kwargs):
        wishlist = Wishlist.objects.filter(user_id=request.user.id)
        self.extra_context = {'wishlist':wishlist,'title':'WishList'}
        return super().get(request, *args, **kwargs)

@login_required
def ItemToWishlist(request,course):

    courseObj = Course.objects.get(id=course)
    Wishlist.objects.create(user_id=request.user,course_id=courseObj).save()
    return HttpResponse(status=204)

class CourseReading(DetailView):
    model = Chapters
    context_object_name = 'chapter'
    template_name = 'User/Course-Reading.html'

    def get(self,request,*args,**kwargs):
        
        try:
            current_chapter = Chapters.objects.get(id = kwargs['pk'])
        except:
            raise ValueError('Some error')
        
        try:
            read = Read_Chapter.objects.get(user=request.user,chapter=current_chapter)
        except:
            read = None
        
        if not read:
            Read_Chapter.objects.create(user=request.user,chapter = current_chapter)

        read_chapters = Read_Chapter.objects.filter(user=request.user)
        
        course_chapters = Chapters.objects.filter(course=current_chapter.course)

        count = 0
        for chapter in course_chapters:
            for read in read_chapters:
                if chapter.id == read.chapter.id:
                    count += 1
        self.extra_context = {'title':'Course Reading'}
        if count == current_chapter.course.chapters:
            self.extra_context['course_completed'] = True

        self.extra_context['is_read'] = read_chapters
        return super().get(request)


class DeleteWishlistItem(DeleteView):
    model = Wishlist
    success_url = '/user/wishlist'

    def get(self,request,*args,**kwargs):
        return self.post(request,args,kwargs)
# cart views

class CartView(TemplateView):
    template_name = 'User/cart.html'

    def get(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.filter(user_id=request.user.id)
        except:
            cart = None

        total = 0

        for item in cart:
            total += item.course_id.price 

        platform_fee = total/100 *10

        grand_total = platform_fee + total 

        razorpay_order_id = 0

        if len(cart) > 0 and cart:
            razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            razorpay_order = razorpay_client.order.create(dict(amount=grand_total*100,currency='INR',payment_capture=1))
            razorpay_order_id = razorpay_order['id']

        self.extra_context = {
            'cart':cart,
            'title':'Cart',
            'total':total,
            'platform_fee': platform_fee,
            'grand_total':grand_total,
            'razorpay_order_id':razorpay_order_id,
            }
        
        return super().get(request, *args, **kwargs)

@csrf_exempt
def razorpay_payment_handler(request):
    if request.method == 'POST':

        razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # verify the payment signature.
        verified = razorpay_client.utility.verify_payment_signature(params_dict)

        if verified:
            carts = Cart.objects.filter(user_id=request.user.id)

            total = 0
            for cart in carts:

                Orders.objects.create(user=request.user,order_id=razorpay_order_id,order_course=cart.course_id)
               
                total += cart.course_id.price / 100 * 10

                cart.delete()

            current_orders = Orders.objects.filter(order_id=razorpay_order_id)
            for order in current_orders:
                order.bill_amount = total
                EnrolledCourse.objects.create(user=request.user,course=order.order_course).save()
                order.order_course.students_enrolled += 1
                order.order_course.save()
                order.save()
           
        return redirect('/user/dashboard')

@login_required
def ItemToCart(request,course):
    courseObj = Course.objects.get(id=course)
    Cart.objects.create(user_id=request.user,course_id=courseObj).save()
    return HttpResponse(status=204)


class DeleteCartItem(DeleteView):
    model = Cart
    success_url = '/user/cart'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    

class EnrolledCourseView(ListView,LoginRequiredMixin):
    login_url = '/user/login/'
    extra_context = {'title':'Enrolled Courses'}
    template_name = 'User/Enrolled-Course.html'
    context_object_name = 'enrolled_courses'

    def get_queryset(self):
        queryset = EnrolledCourse.objects.filter(user=self.request.user)
        return queryset    

@login_required
def add_comment(request,chapter_id):
    current_chapter = Chapters.objects.get(id=chapter_id)
    current_comment = request.POST.get('comment')
    Comment.objects.create(chapter=current_chapter,user=request.user,comment=current_comment)
    return redirect(f'/user/course-reading/{chapter_id}')

@login_required
def reply_comment(request,chapter_id,comment_id):

    current_chapter = Chapters.objects.get(id=chapter_id)
    parent_comment = Comment.objects.get(id=comment_id)
    current_comment = request.POST.get('comment')
    Comment.objects.create(chapter=current_chapter,user=request.user,comment=current_comment,reply_comment=parent_comment)
    return redirect(f'/user/course-reading/{chapter_id}')

@login_required
def add_review(request,course_id):
    try:       
        current_course = Course.objects.get(id=course_id)
        user_rating = request.POST.get('star_rating')
        user_review = request.POST.get('review')

    except:
        raise ValueError('Some error occured')

    Review.objects.create(course = current_course,user=request.user,review_text=user_review,rating=user_rating)
    return redirect(f'/course-details/{course_id}')

@login_required
def delete_review(request,review_id,course_id):
    try:
        Review.objects.get(id=review_id).delete()
    except:
        print('error')

    return redirect(f'/user/course-reading/{course_id}')

# def download_certificate(request):
#     pdf_path = os.path.join(settings.BASE_DIR, 'Templates', 'certificate_pdf.pdf')

#     pdf_file = open(pdf_path, 'rb')

#     response = FileResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

#     return response

@login_required
def download_certificate(request,course_id):

    course = Course.objects.get(id=course_id)
    course_name = course.title
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    template = get_template('Certificate.html')
    html = template.render({'name':request.user.first_name + ' ' + request.user.last_name , 'course':course_name})

    pisa_status = pisa.CreatePDF(html,dest=response)


    return response


