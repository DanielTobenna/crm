from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
	path('register/', views.registerpage, name='register'),
	path('login/', views.loginpage, name='login'),
	path('logout/', views.logoutuser, name='logout'),
	path('', views.home, name='home'),
	path('user_profile/', views.userprofile, name='user_profile'),
	path('account_settings/', views.accountSettings, name='account_settings'),
	path('products/', views.products, name='products'),
	path('customer/<str:pk>/', views.customer, name='customer'),
	path('create_order/<str:pk>/', views.createOrder, name='create_order'),
	path('update_order/<str:pk>/', views.UpdateOrder, name='update_order'),
	path('delete_order/<str:pk>/', views.DeleteOrder, name='delete_order'),


	#Django built in methods to send password reset email

	path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='reset_password'),

	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), name='reset_password_sent'),

	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'), name='password_reset_confirm'),

	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_complete'),

	#now head over and configure email sending in your settings.py file
]