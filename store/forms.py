from django import forms
from django.contrib.auth.models import User
from .models import Address
class RegisterForm(forms.Form):
 username=forms.CharField(max_length=150); email=forms.EmailField()
 password=forms.CharField(widget=forms.PasswordInput,min_length=8)
 confirm_password=forms.CharField(widget=forms.PasswordInput)
 def clean_username(self):
  v=self.cleaned_data['username']
  if User.objects.filter(username=v).exists(): raise forms.ValidationError('Username already exists.')
  return v
 def clean_email(self):
  v=self.cleaned_data['email']
  if User.objects.filter(email__iexact=v).exists(): raise forms.ValidationError('Email already registered.')
  return v
 def clean(self):
  d=super().clean()
  if d.get('password') and d.get('confirm_password') and d['password']!=d['confirm_password']: self.add_error('confirm_password','Passwords do not match.')
  return d
class AddressForm(forms.ModelForm):
 class Meta:
  model=Address
  fields=['full_name','phone','line1','line2','city','state','postal_code','is_default']
