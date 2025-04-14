from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True,
        next_page='accounts:profile'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/',
        http_method_names=['post', 'get']
    ), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('pokedex/', views.pokedex, name='pokedex'),
] 