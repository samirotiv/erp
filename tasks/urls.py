from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^addtask/$', 'tasks.views.add_task'),
                       
                       
#  url(r'^addcopy/$', 'libauth.views.AddCopy'),
# url(r'^updatecopy/(?P<primkey>\d+)/$', 'libauth.views.UpdateCopy'),
)
