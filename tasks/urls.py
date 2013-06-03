from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^add/$', 'tasks.views.add_intra_task'),
    url(r'^addx/$', 'tasks.views.add_cross_task'),  
    url(r'^edit/(?P<primkey>\d+)/$', 'tasks.views.edit_intra_task'),                    
    url(r'^editx/(?P<primkey>\d+)/$', 'tasks.views.edit_cross_task'),
                                          
#  url(r'^addcopy/$', 'libauth.views.AddCopy'),
# url(r'^updatecopy/(?P<primkey>\d+)/$', 'libauth.views.UpdateCopy'),
)
