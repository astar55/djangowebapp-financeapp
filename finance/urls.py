from django.conf.urls import url

from . import views

app_name = 'finance'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^details/$', views.details, name='details'),
]