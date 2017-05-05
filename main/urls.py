from django.conf.urls import url

from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.Main, name='Main'),
    url(r'^insert/$', views.NewFile, name='New File'),
    url(r'^insert/link/$', views.NewLink, name='New Link'),
    url(r'^insert/successfully/$', views.File_saved, name='File saved'),
    url(r'^download/(?P<file_id>\d+)/$', views.Download_file, name='File download'),
    url(r'^overview/$', views.Overview, name='My publication'),
    url(r'^overview/delete/(?P<file_id>\d+)/$', views.Delete_file, name='Delete file'),
    url(r'^overview/changeStatus/(?P<file_id>\d+)/$', views.Status_file, name='Change status file'),
    url(r'^settings/$', views.Settings, name='Account settings'),
    url(r'^overview/update/(?P<file_id>\d+)/$', views.Update_file, name='Update file'),

]