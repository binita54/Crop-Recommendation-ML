from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('signup/', signup_view, name='signup'),
    path('predict/', predict_view, name='predict'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('history/', user_history_view, name='user_history'),
    path('history_delete/<int:id>/', user_delete_prediction, name='user_delete_prediction'),
    path('profile/', profile_view, name='profile'),
    path('change_password/', change_password_view, name='change_password'),
    path('admin_login/', admin_login_view, name='admin_login'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),

]