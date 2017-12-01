from django.conf.urls import url
from django.views.generic import RedirectView

from transactions import views

urlpatterns = [
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^', RedirectView.as_view(pattern_name='dashboard'))
]
