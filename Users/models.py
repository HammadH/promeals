from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import signals
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string




class UserManager(BaseUserManager):
	def create_user(self, full_name, free_meal_package, email, password, mobile, address):
			new_user = self.model(full_name=full_name, free_meal_package=free_meal_package, email=email,
								mobile=mobile, address=address)
			new_user.set_password(password)
			try:
				new_user.save()
				return new_user
			except Exception, e:
				print e 
				return None
					
	def create_superuser(self, email, password, mobile):
		new_user = self.model(email=email)
		new_user.set_password(password)
		new_user.mobile = mobile
		new_user.is_superuser = True
		new_user.save()
		return new_user

	def activate_user(self, user):
		user.is_active=True
		#send signal to me 
		user.save()
		return True

 # send_mail(subject, message, from_email, recipient_list, fail_silently=False, 
 # 	auth_user=None, auth_password=None, connection=None, html_message=None)
	
	
	def user_registered_notification_email(self, superuser, user):
		pass

	def user_activated_notification_email(self, superuser, user):
		pass


class User(AbstractBaseUser, PermissionsMixin):
	full_name = models.CharField(max_length=100, blank=False)
	email = models.EmailField(unique=True, blank=False)
	free_meal_package = models.CharField(blank=False, max_length=40, null=True)
	mobile = models.CharField(unique=True, blank=False, max_length=10)
	address = models.TextField()

	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['mobile']
	objects = UserManager()

	def __unicode__(self):
		return self.full_name

	def get_full_name(self):
		return self.full_name

	def get_short_name(self):
		return self.full_name

	def get_mobile(self):
		return self.mobile

	def get_address(self):
		return self.address

	def get_email(self):
		return self.email

	def has_package(self):
		if self.package.get():
			return True
		else: return False

	def get_package(self):
		if self.package.get():
			return self.package.get()
		else:
			return None

	def is_package_active(self):
		if self.package.get().payment_status == 1:
			return True
		else: return False


def send_activation_email(sender, instance, created, **kwargs):
		if created:
			subject = "New Customer Registered"
			message = render_to_string('email_message.html', {'user':instance})
			from_email = "hello@feastymeals.com"                 #common email to send out emails from feastymeals
			recipient_list = ['registrations@feastymeals.com']   #this will be my email for user infos
			
			subject_to_user = "Hello there!"
			message_to_user = render_to_string('user_email_message.html', {'user':instance})
			recipient_user = [instance.email]
			try:
				print "new user created"
				send_mail(subject, message, from_email, recipient_list)
				send_mail(subject_to_user, message_to_user, from_email, recipient_user )
				
			except Exception, e:
				print e
				
		else:
			return
		




signals.post_save.connect(send_activation_email, User, dispatch_uid= "new user registration")




admin.site.register(User)


