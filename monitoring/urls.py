from django.urls import path
from .views import dashboard
from django.contrib.auth import views as auth_views
from .views import dashboard, register_view  # add register_view here
from . import views 


urlpatterns = [

     path('dashboard/', dashboard, name='dashboard'),
     path('api/latest-data/', views.latest_grid_data, name='latest_data'),
    # Login view
    path('login/', auth_views.LoginView.as_view(
        template_name='monitoring/login.html',
        redirect_authenticated_user=True  # redirect logged-in users automatically
    ), name='login'),

    # Logout view
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'  # redirect to login after logout
    ), name='logout'),
     path('register/', register_view, name='register'),
     path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('inject-attack/', views.inject_attack, name='inject_attack'),
    path('api/grid-data/', views.GridDataAPI.as_view(), name='grid_data_api'),


]

