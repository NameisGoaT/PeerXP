from django.urls import path
from support_app import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_department/', views.create_department, name='create_department'),
    path('manage_tickets/', views.manage_tickets, name='manage_tickets'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
]
