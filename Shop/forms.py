from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from.models import customer

class CustomerRegistrationForm(UserCreationForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': "Enter your Email"}
        # labels = {'username': forms.Textarea(attrs={'class': 'form-control'})}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}
#Login
class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password=forms.CharField(label='Password',strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current_password','class':'form-control'}))

#PASSWORDCHANGE FORM
class mypasswordchange(PasswordChangeForm):
    old_password=forms.CharField(label=_('Old Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current_password','autofocus':True,'class':'form-control'}))

    new_password1=forms.CharField(label=_('New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html)

    new_password2=forms.CharField(label=_('Confrim New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new password','class':'form-control'}))

#PASSWORD RESET
    
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control'}))
    
#set password form
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    
    new_password2 = forms.CharField(label=_('Confirm new password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}))


#profile
    
class customerprofile(forms.ModelForm):
    class Meta:
        model=customer
        fields=['name','division','district','thana','vllorroad','zipcode']
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),'division': forms.Select(attrs={'class':'form-control'}),'district':forms.TextInput(attrs={'class':'form-control'}),'thana':forms.TextInput(attrs={'class':'form-control'}),'vllorroad':forms.TextInput(attrs={'class':'form-control'}),'zipcode':forms.NumberInput(attrs={'class':'form-control'})}
