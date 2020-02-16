from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	#path('login/', views.login, name='login'),
	path('login/', auth_views.LoginView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),

	path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
	path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

	path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

	path('registration/', views.user_registration, name='user_registration'),
	path('edit/', views.user_edit, name='user_edit'),
	path('', views.feed, name='feed'),

	path('follow/', views.user_follow, name='follow'),
	path('<username>/', views.user_detail, name='user'), #Поменять на другой шаблон
	path('users/', views.user_list, name='users'),
]