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
    re_path(r'^plea/(?P<pk>\d+)/delete/$', views.PleaDelete.as_view(), name='plea_delete'),
]