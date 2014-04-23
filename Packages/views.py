from django.shortcuts import render_to_response
from django.views.generic import View
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect

from Packages.models import Package
from Packages.forms import PackageForm

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class PackageSelectView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		return render_to_response('packageselect.html', {'packageForm':PackageForm()}, RequestContext(request))

	def post(self, request, *args, **kwargs):
		
		package_form = PackageForm(request.POST)
		if package_form.is_valid():
			user = request.user
			package_type=package_form.cleaned_data['package_type']
			package_billing_type = package_form.cleaned_data['package_billing_type']
			new_package = Package.objects.create_new_package(user, package_type, package_billing_type)
			if new_package is not None:
				return HttpResponse('ok')
			else:
				return HttpResponse('is none')
		else:
			return HttpResponse('package_form is invalid')




