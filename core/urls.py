from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('search/', views.search_results, name='search_results'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('help/', views.help, name='help'),
    path('questions/', views.question_list, name='question_list'),
    path('questions/<int:pk>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask_question'),
]
