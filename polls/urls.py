from django.conf.urls import url

from . import views

app_name = 'polls'

urlpatterns = [
    url(r'^$', views.Login, name='Login'),
    url(r'^register/$', views.Register, name='Register'),


]