from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from Users.views import RegistrationView, LoginView, LogoutView, AccountView



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'food.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^myaccount/', AccountView.as_view(), name='myaccount'),
    url(r'^register/', RegistrationView.as_view(), name='registration'),
    
) 

