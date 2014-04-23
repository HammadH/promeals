import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from Users.models import User


PACKAGE_TYPE = (('Indian','Indian'),
				('Pakistani','Pakistani'),
				('Mixed','MIXED'),)



def check_mobile(mobile):
	format = re.compile('(^[0-9]{10}$)')
	if format.match(mobile) != None:
		return True
	else: return False


class AuthForm(AuthenticationForm):
	username = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}), max_length=254, label='')
	password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder':'Password'}))




class UserRegistrationForm(forms.ModelForm):
	full_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your full name'}))
	email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Activation email will be sent'}))
	password = forms.CharField(widget=forms.PasswordInput)
	address = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))
	free_meal_package = forms.ChoiceField(choices=PACKAGE_TYPE, widget=forms.RadioSelect())
	mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'You will recieve a call on this number'}))
	address = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Your complete address to deliver the meal', 'rows':'3'}))
	class Meta:
		model = User
		fields = ['full_name', 'email', 'password', 'free_meal_package' ,'mobile', 'address']

	def clean_mobile(self):
		mobile_no = self.cleaned_data['mobile']

		if check_mobile(mobile_no):
			return mobile_no
		else:
			raise forms.ValidationError(u"Please enter a valid mobile number. Eg: 0551231231")

	def clean_email(self):
		email = self.cleaned_data['email']
		from Users.models import User
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("Email already exists!")
		return email