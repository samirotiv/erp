from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'erp.views.home', name='home'),
    # url(r'^erp/', include('erp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/', include('tasks.urls')),
    url(r'^login/$', 'users.views.login'),
    url ( r'^choose_identity/$', 'users.views.choose_identity'),
    url(r'^logout/$', 'users.views.logout'),
    url(r'^dash/$', 'dash.views.dash_view'),
)
