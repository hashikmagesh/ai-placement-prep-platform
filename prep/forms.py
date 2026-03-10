from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username',max_length=100,required=True)
    email = forms.EmailField(label='Email',max_length=100,required=True)
    password = forms.CharField(label='Password',max_length=100,required=True)
    password_confirm = forms.CharField(label='Confirm_Password',max_length=100,required=True)

    class Meta:
        model = User
        fields = ['username','email','password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password!=password_confirm:
            raise forms.ValidationError("Mismatch Password")
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=100,required=True)
    password = forms.CharField(label='Password',max_length=100,required=True)

    def clean(self):
        cleaned_data =super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username,password=password)
            if user is None:
                raise forms.ValidationError('Invalid username or password')
            
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email',max_length=100,required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Use Valid Email_id")
        
class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label="new_password", max_length=240, required=True)
    confirm_password = forms.CharField(label="confirm_password", max_length=240, required=True)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password  and  new_password!=confirm_password:
            raise forms.ValidationError('Invalid password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_image',
            'phone_number',
            'college_name',
            'branch',
            'graduation_year',
            'linkedin_url',
            'github_url',
            'portfolio_url',
            'resume_file',
            'target_domain',
            'target_company',
            'bio',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }