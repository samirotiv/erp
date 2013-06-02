from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^addtask/$', 'tasks.views.add_intra_task'),
    url(r'^addxtask/$', 'tasks.views.add_cross_task'),  
    url(r'^edittask/(?P<primkey>\d+)/$', 'tasks.views.edit_intra_task'),                    
    url(r'^editxtask/(?P<primkey>\d+)/$', 'tasks.views.edit_cross_task'),
                                          
#  url(r'^addcopy/$', 'libauth.views.AddCopy'),
# url(r'^updatecopy/(?P<primkey>\d+)/$', 'libauth.views.UpdateCopy'),
)
