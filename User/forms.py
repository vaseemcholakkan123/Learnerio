from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from User.models import User
from django.contrib.auth import authenticate,login
from django import forms
from Tutor.models import Tutor,Skills

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class BecomeTutor(forms.ModelForm):
    mobile = forms.CharField(max_length=10)
    skills = forms.ModelMultipleChoiceField(queryset=Skills.objects.all(),widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Tutor
        fields = ('qualification','skills','mobile')


class LoginForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get('username',None)
        password = self.cleaned_data.get('password',None)

        try:
            user_exists = User.objects.get(username=username)
        except:
            user_exists = None

        if user_exists:
            if user_exists.is_active and not user_exists.is_blocked:
                user_cache = authenticate(self.request,username=username,password=password)
                if user_cache:
                    login(self.request,user_cache)
                else:
                    raise forms.ValidationError('Wrong password for the user',code='password_wrong')

            elif not user_exists.is_active:
                raise forms.ValidationError('User Not Verified',code='user_not_verified')
            else:
                raise forms.ValidationError('User Blocked',code='user_blocked')
        else:
            raise forms.ValidationError('No such user',code='user_not_found')


class UserUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'custom-file-input'}))

    class Meta:
        model = User
        fields = ('username','first_name','last_name','profile_pic','email','date_of_birth')