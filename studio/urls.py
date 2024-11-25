from . import views
from django.urls import re_path
from django.urls import path

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path('register/', views.sign_up, name='register'),
    path('loginuser/', views.sign_in, name='loginuser'),
    re_path(r'^plea/create/$', views.plea_create, name='plea_create'),
    re_path(r'^plea/(?P<pk>\d+)$', views.PleaDetailView.as_view(), name='plea-detail'),
    re_path(r'^pleas/$', views.PleaListView.as_view(), name='pleas'),
    re_path(r'^pleasn/$', views.PleaListViewN.as_view(), name='pleas_n'),
    re_path(r'^pleasc/$', views.PleaListViewC.as_view(), name='pleas_c'),
    re_path(r'^pleasi/$', views.PleaListViewI.as_view(), name='pleas_i'),
    re_path(r'^plea/(?P<pk>\d+)/delete/$', views.PleaDelete.as_view(), name='plea_delete'),
    re_path(r'^inactives/$', views.UserListView.as_view(), name='inactives'),
    re_path(r'^inactive/(?P<pk>\d+)/activate/$', views.activate_user, name='user_activate'),
]