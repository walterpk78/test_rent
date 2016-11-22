__author__ = 'walter'
from django.conf.urls import url
from . import views
from . import ajax

# We are adding a URL called /home
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^rent/',  views.rent,    name='rent'),
    url(r'^help/',  views.help,    name='help'),
    url(r'^list/',  views.list,    name='list'),
    url(r'^info/',  views.info,    name='info'),
    url(r'^list_ajax/',  ajax.list,    name='list_ajax'),
    url(r'^pay/',  views.pay,    name='pay'),
]