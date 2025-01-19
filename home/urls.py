from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Blog URLs
    path('blog/create/', views.blogpost, name='blogpost'),
    path('blog/<int:blog_id>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:blog_id>/delete/', views.blog_delete, name='blog_delete'),
    path('donate/<int:blog_id>/', views.donate, name='donate'),
    path('approve-donations/', views.approve_donations, name='approve_donations'),

    # Event URLs
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('events/participants/', views.event_participants, name='event_participants'),
    path('events/<int:event_id>/remove-participant/<int:participant_id>/', views.remove_participant, name='remove_participant'),
    path('event/<int:event_id>/join/', views.join_event, name='join_event'),
    path('event/<int:event_id>/freeze/', views.freeze_event, name='freeze_event'),

]
