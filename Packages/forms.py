from django import forms

from Packages.models import Package

class PackageForm(forms.ModelForm):
	class Meta:
		model = Package
		fields = ['type', 'billing_type']