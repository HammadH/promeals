import os

from django.db import models
from django.contrib import admin
from Users.models import User



PACKAGE_TYPE = (('I','Indian'),
				('P','Pakistani'),
				('Mixed','MIXED'),)

PACKAGE_BILLING_TYPE = (('1W', '1 Week'),
						('2W', '2 Weeks'),
						('3W', '3 Weeks'),
						('1M', '1 Month'))
						
PAYMENT_STATUS = (('1','PAID'),
				  ('0','NOT-PAID'))

# MENU_TYPE = ('I':'Indian',
# 			 'P':'Pakistani')

def get_promo_image_path(instance, filename):
	return os.path.join('Promotion', '%s' %instance, '%s' %filename)


class Promotion(models.Model):
	name = models.CharField(max_length=50, unique=True)
	is_active = models.BooleanField(default=False)
	date = models.DateTimeField(blank=True, null=True)
	image = models.ImageField(upload_to=get_promo_image_path)

	def __unicode__(self):
		return self.name

class PackageManager(models.Manager):
	def create_new_package(self, user, package_type, package_billing_type):
		new_package=self.model(user=user, type=package_type, billing_type=package_billing_type)
		try:
			new_package.save()
			return new_package
		except Exception, e:
			print e
			return None






class Package(models.Model):
	type = models.CharField(max_length="20",choices=PACKAGE_TYPE, blank=False)
	user = models.ForeignKey(User, unique=True, related_name='package')	
	purchased_on = models.DateTimeField(auto_now_add=True)
	changed_on = models.DateTimeField(blank=True, null=True)
	ends_on = models.DateTimeField(blank=True, null=True)
	billing_type = models.CharField(max_length="20",choices= PACKAGE_BILLING_TYPE, default=PACKAGE_BILLING_TYPE[2], blank=False)
	payment_status = models.CharField(max_length="20", choices=PAYMENT_STATUS, default=PAYMENT_STATUS[1])
	#package expring alert
     
	objects = PackageManager()    
	def __unicode__(self):
		return self.type





admin.site.register(Package)
admin.site.register(Promotion)
# class Menu(models.Model):
# 	menu_type = models.ChoiceField()


# class Meal(models.Model):
# 	name = models.CharField(max_length=100, blank=False)
    














