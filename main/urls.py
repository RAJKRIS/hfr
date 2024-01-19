

from django.urls import path
from django.views.generic import TemplateView

from main import views

urlpatterns = [
    path("success/", TemplateView.as_view(template_name="main/success.html")),
    path("error/", TemplateView.as_view(template_name="main/error.html")),
    path("sign-in/", TemplateView.as_view(template_name="main/login.html")),
    path("register/", TemplateView.as_view(template_name="main/home.html")),
    path("register_new_user/", views.register_new_user, name='register_new_user'),
    path("login/", views.login, name='login'),
]

