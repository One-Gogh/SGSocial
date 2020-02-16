from django.urls import path
from . import views 

urlpatterns = [
	path('', views.list_liked_images, name='list_liked_images'),
	path('add/', views.add_image, name='add_image'),
	path('detail/<int:id>/<slug:slug>/', views.detail_image, name='detail_image'),
	path('like/', views.like_image, name='like_image'),
	path('all_images/', views.all_images, name='all_images')
]