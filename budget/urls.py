from django.conf.urls import url

from budget import views

app_name = 'budget'
urlpatterns = [
    url(r'^expense/$', views.CreateExpenseView.as_view(), name='create-expense'),
    url(r'^expense/(?P<pk>\d+)/$', views.UpdateExpenseView.as_view(), name='update-expense'),
    url(r'^expenses/$', views.ListExpenseView.as_view(), name='expense-list'),
]
