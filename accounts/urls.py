from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import home_view  # Импортирайте вашето view
app_name = 'accounts'
urlpatterns = [
    path('', home_view, name='home'),

    # Пътища за автентикация
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:home'), name='logout'),
]
