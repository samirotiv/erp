from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('home.views',
    # Examples:
    # url(r'^$', 'erp.views.home', name='home'),
    # url(r'^erp/', include('erp.foo.urls')),
    url ( r'^$', 'homepage' ),
    url ( r'^choose_identity/$', 'choose_identity'),
)
