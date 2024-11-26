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
    re_path(r'^inactive/(?P<pk>[-\w]+)/activate/$', views.activate_user, name='activate_user'),
    re_path(r'^categorys/$', views.CategoryListView.as_view(), name='categorys'),
    re_path(r'^category/(?P<pk>\d+)/delete/$', views.CategoryDelete.as_view(), name='category_delete'),
    re_path(r'^category/(?P<pk>\d+)$', views.CategoryDetailView.as_view(), name='category-detail'),
    re_path(r'^category/create/$', views.CategoryCreateView.as_view(), name='category_create'),
    re_path(r'^adminpleas/$', views.AdminPleaListView.as_view(), name='adminpleas'),
    re_path(r'^plea/(?P<pk>\d+)/complete/$', views.PleaAddDesign.as_view(), name='plea_complete'),
]