from django.conf.urls import patterns, include, url
from Packages.views import PackageSelectView


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'food.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^selectP/', PackageSelectView.as_view(), name='selectPackage'),

    )