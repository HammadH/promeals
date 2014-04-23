import json

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from Users.forms import UserRegistrationForm
from Users.models import User
from Packages.models import Package
from Packages.forms import PackageForm


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)



class RegistrationView(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('registration.html', {'form': UserRegistrationForm()}, RequestContext(request))

	def post(self, request, *args, **kwargs):
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
			return HttpResponse(json.dumps(new_user))
		else:
			return HttpResponse('invalid form')
		

class LoginView(FormView):
	template_name='login.html'
	form_class=AuthenticationForm
	success_url= '/users/myaccount/'

	def form_valid(self, form):
		email = form.cleaned_data['username']
		password = form.cleaned_data['password']
		try:
			user = authenticate(username=email, password=password)
			if user is not None:
				if user.is_active:
					login(self.request, user)
					return HttpResponseRedirect('/users/myaccount/')
				else:
					return HttpResponse('please activate account')
			else:
				return HttpResponse('user is none')

		except Exception, e:
			return HttpResponse(e) 

class LogoutView(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		return HttpResponseRedirect('/')


class AccountView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		context = {}
		try:
			context['package']= request.user.package.get()
		except Package.DoesNotExist:
			context['package_message']= u"you do not have any package"
			context['packageForm'] = PackageForm()
		
		return render_to_response('account.html', context, RequestContext(request))


	def post(self, request, *args, **kwargs):
		pass

	

		

