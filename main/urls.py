from django.conf.urls import url

from . import views

app_name = 'main'

urlpatterns = [
    url(r'^$', views.Main, name='Main'),
    url(r'^insert/$', views.NewFile, name='New File'),
    url(r'^insert/successfully/$', views.File_saved, name='File saved'),
    url(r'^overview/$', views.Overview, name='My publication'),
    url(r'^overview/delete/(?P<file_id>\d+)/$', views.Delete_file, name='Delete file'),

]