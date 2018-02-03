from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView

from core import views

urlpatterns = [
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^login/$', LoginView.as_view(template_name='core/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='core/logout.html'), name='logout'),

    url(r'^transaction/debit/$', views.CreateDebitTransactionView.as_view(), name='new-debit-transaction'),
    url(r'^transaction/debit/(?P<pk>\d+)/$', views.UpdateDebitTransactionView.as_view(), name='update-debit-transaction'),

    url(r'^transaction/credit/$', views.CreateCreditTransactionView.as_view(), name='new-credit-transaction'),
    url(r'^transaction/credit/(?P<pk>\d+)/$', views.UpdateCreditTransactionView.as_view(), name='update-credit-transaction'),
    url(r'^transaction/(?P<pk>\d+)/$', views.update_transaction, name='update-transaction'),

    url(r'^transfer/user/$', views.new_transfer_to_user, name='transfer-user'),
    url(r'^transfer/account/$', views.new_transfer_to_account, name='transfer-account'),
    url(r'^transfer/bucket/$', views.CreateTransferToBucketView.as_view(), name='transfer-bucket'),

    url(r'^accounts/$', views.ListAccountView.as_view(), name='account-list'),
    url(r'^account/$', views.CreateAccountView.as_view(), name='create-account'),
    url(r'^account/(?P<pk>\d+)/$', views.UpdateAccountView.as_view(), name='update-account'),
    url(r'^inbox-account/(?P<pk>\d+)/$', views.UpdateInboxAccountView.as_view(), name='update-inbox-account'),
    url(r'^buckets/$', views.ListBucketView.as_view(), name='bucket-list'),
    url(r'^bucket/$', views.CreateBucketView.as_view(), name='create-bucket'),
    url(r'^bucket/(?P<pk>\d+)/$', views.UpdateBucketView.as_view(), name='update-bucket'),
    url(r'^$', RedirectView.as_view(pattern_name='dashboard'))
]
