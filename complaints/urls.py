from django.urls import path
from . import views

urlpatterns = [
    
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Public page
    path('public-eye/', views.public_eye, name='public_eye'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Complaint features
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),

    # View complaint
    path('complaint/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),

    # Edit complaint
    path('complaint/<int:complaint_id>/edit/', views.edit_complaint, name='edit_complaint'),

    # Delete complaint
    path('complaint/<int:complaint_id>/delete/', views.delete_complaint, name='delete_complaint'),

    # Admin features
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update-status/<int:id>/', views.update_status, name='update_status'),
    path('reports/', views.reports, name='reports'),
path('profile/', views.profile, name='profile'),
    # Forgot password
    path('forgot-password/', views.forgot_password, name='forgot_password'),
        path('notifications/', views.user_notifications, name='notifications'),
path(
    'notifications/read/<int:pk>/',
    views.mark_notification_read,
    name='mark_notification_read'
),
]