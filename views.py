from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext

from Users.models import User
from Users.forms import UserRegistrationForm, AuthForm
from Packages.models import Promotion







class HomeView(View):
	def get(self, request, *args, **kwargs):
		context = self.get_context()
		return render_to_response('landing.html', context, RequestContext(request))



	def post(self, request, *args, **kwargs):
		if 'username' in request.POST:
			loginForm = AuthenticationForm(request.POST)
			if loginForm.is_valid():
				
				user = authenticate(loginForm.cleaned_data['username'], loginForm.cleaned_data['password'])
				if user is not None:
					if user.is_active():
						return HttpResponseRedirect('/users/myaccount/')
					else: return HttpResponse('Please activate your account!')
				else: return HttpResponse('Incorrect email/password')	
			else: return StreamingHttpResponse(loginForm.fields.values())
			
		else:
			form = UserRegistrationForm(request.POST)
			if form.is_valid():
				full_name = form.cleaned_data['full_name']
				free_meal_package = form.cleaned_data['free_meal_package']
				email = form.cleaned_data['email']
				password = form.cleaned_data['password']
				address = form.cleaned_data['address']
				mobile = form.cleaned_data['mobile']
				new_user = User.objects.create_user(full_name, free_meal_package, email, password, mobile, address)
				new_user.save()
				return HttpResponse('ok')
			else:
				context = self.get_context()
				context['registrationForm'] = UserRegistrationForm(request.POST)
				return render_to_response('landing.html',  context, RequestContext(request))


	def get_context(self):
		try:
			freemeal = Promotion.objects.get(name='freemeal')
			context = {
				'loginForm': AuthForm(),
				'registrationForm': UserRegistrationForm(),
				'freemeal': freemeal
				}
		except Exception, e:
			print e
			context = {
				'loginForm': AuthForm(),
				'registrationForm': UserRegistrationForm(),
				}
		return context
