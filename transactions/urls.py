from django.conf.urls import url
from django.views.generic import RedirectView

from transactions import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^transaction/$', views.new_transaction, name='new_transaction'),
    url(r'^transfer/user/$', views.new_transfer_to_user, name='transfer-user'),
    url(r'^transfer/account/$', views.new_transfer_to_account, name='transfer-account'),
    url(r'^transfer/bucket/$', views.CreateTransferToBucketView.as_view(), name='transfer-bucket'),
    url(r'^transaction/(?P<pk>\d+)/$', views.edit_transaction, name='edit_transaction'),
    url(r'^accounts/$', views.ListAccountView.as_view(), name='account-list'),
    url(r'^account/$', views.CreateAccountView.as_view(), name='create-account'),
    url(r'^account/(?P<pk>\d+)/$', views.UpdateAccountView.as_view(), name='update-account'),
    url(r'^inbox-account/(?P<pk>\d+)/$', views.UpdateInboxAccountView.as_view(), name='update-inbox-account'),
    url(r'^buckets/$', views.ListBucketView.as_view(), name='bucket-list'),
    url(r'^bucket/$', views.CreateBucketView.as_view(), name='create-bucket'),
    url(r'^bucket/(?P<pk>\d+)/$', views.UpdateBucketView.as_view(), name='update-bucket'),
    url(r'^$', RedirectView.as_view(pattern_name='dashboard'))
]
