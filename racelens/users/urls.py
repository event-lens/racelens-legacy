from django.urls import path
from django.conf.urls import url

from . import views

app_name = "users"

urlpatterns = [
    url('login/', views.login_view, name="login"),
    url('logout/', views.logout_view, name="logout"),
    url('register/', views.register_view, name="register")
]