from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
	first_password = forms.CharField(label='Password', widget=forms.PasswordInput)
	second_password = forms.CharField(label='Password again', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email')

	def clean_email(self): 
		if self.cleaned_data['email']:
			email = self.cleaned_data['email']

			if User.objects.filter(email=email).exists():
				raise forms.ValidationError('Email exists')
		else:
			return self.cleaned_data

	def clean_second_password(self):
		cd = self.cleaned_data
		if cd['first_password'] != cd['second_password']:
			raise forms.ValidationError('Password don\'t match.')
		else:
			return cd['second_password']

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('date_of_birth', 'photo')