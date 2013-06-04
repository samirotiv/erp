from django.conf.urls import patterns, include, url


urlpatterns = patterns('tasks.views',
    url(r'(?P<primkey>\d+)/$', 'display_task'),
    url(r'^add/$', 'add_intra_task'),
    url(r'^addx/$', 'add_cross_task'),  
    url(r'^edit/(?P<primkey>\d+)/$', 'edit_task'),                    
                                          
#  url(r'^addcopy/$', 'libauth.views.AddCopy'),
# url(r'^updatecopy/(?P<primkey>\d+)/$', 'libauth.views.UpdateCopy'),
)
