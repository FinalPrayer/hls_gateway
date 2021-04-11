from django.urls import path

from channels import views

urlpatterns = [
    path('admin/list/', views.channel_list, name='channel_list'),
    path('admin/add/', views.channel_add, name='channel_add'),
    path('admin/del/<str:channel>/', views.channel_del, name='channel_del'),
    path('watch/<str:nickname>', views.channel_open, name='channel_open'),
    path('read/<str:channel>/<str:filename>', views.channel_read, name='channel_read'),
]
