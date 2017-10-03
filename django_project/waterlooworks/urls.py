from django.conf.urls import url
from . import views

app_name = 'waterlooworks'

urlpatterns = [
    url(r'^$', views.main_index, name="main_index"),
    url(r'^jobs/$', views.JobsListView.as_view(), name="index"),
    url(r'^jobs/(?P<pk>[0-9]+)/update/$', views.JobsUpdateView.as_view(), name="job_update"),
    url(r'^jobs/(?P<pk>[0-9]+)/$', views.JobsDetailView.as_view(), name="job_detail"),
]