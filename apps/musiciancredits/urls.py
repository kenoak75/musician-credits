from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dashboard),
    url(r'^log$', views.log),
    url(r'^reg$', views.reg),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^add_recording$', views.add_recording),
    url(r'^update/(?P<recording_id>\d+)$', views.update),
    url(r'^edit/(?P<user_id>\d+)$', views.edit),
    url(r'^edit_account/(?P<user_id>\d+)$', views.edit_account),
    url(r'^edit_recording/(?P<recording_id>\d+)$', views.edit_recording),
    url(r'^delete/(?P<recording_id>\d+)$', views.delete),

]