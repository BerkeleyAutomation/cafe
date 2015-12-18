from django.conf.urls.defaults import *
import opinion.settings
exec "from phone import views_%s as views" % opinion.settings.PHONE_MODULE

urlpatterns = patterns(
    '',
    url(r'^$', views.begin),
    url(r'^begin/$', views.begin),
    url(r'^save_edu_center/$', views.save_edu_center),
    url(r'^statement/(\d+)/', views.statement),
    # url(r'^demographic/', views.demographic),
    url(r'^peer_rate/(\d+)/(\d+)/', views.peer_rate),
    url(r'^record_comment/', views.record_comment),
    url(r'^finish/', views.finish),
)
