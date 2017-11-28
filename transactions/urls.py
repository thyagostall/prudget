from django.conf.urls import url

from transactions import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
]
