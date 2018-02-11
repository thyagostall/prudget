from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView

import core.views.create_transfer_to_bucket_view
import core.views.create_account_view
import core.views.create_bucket_view
import core.views.create_credit_transaction_view
import core.views.create_debit_transaction_view
import core.views.create_transfer_to_account_view
import core.views.create_transfer_to_user_view
import core.views.dashboard_view
import core.views.list_account_view
import core.views.list_bucket_view
import core.views.update_account_view
import core.views.update_bucket_view
import core.views.update_credit_transaction_view
import core.views.update_debit_transaction_view
import core.views.update_inbox_account_view
import core.views.update_transaction_view
from core import views

urlpatterns = [
    url(r'^login/$', LoginView.as_view(template_name='core/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='core/logout.html'), name='logout'),

    url(r'^dashboard/$', core.views.dashboard_view.dashboard, name='dashboard'),

    url(r'^transaction/debit/$', core.views.create_debit_transaction_view.CreateDebitTransactionView.as_view(), name='new-debit-transaction'),
    url(r'^transaction/debit/(?P<pk>\d+)/$', core.views.update_debit_transaction_view.UpdateDebitTransactionView.as_view(), name='update-debit-transaction'),

    url(r'^transaction/credit/$', core.views.create_credit_transaction_view.CreateCreditTransactionView.as_view(), name='new-credit-transaction'),
    url(r'^transaction/credit/(?P<pk>\d+)/$', core.views.update_credit_transaction_view.UpdateCreditTransactionView.as_view(), name='update-credit-transaction'),
    url(r'^transaction/(?P<pk>\d+)/$', core.views.update_transaction_view.update_transaction, name='update-transaction'),

    url(r'^transaction/toggle/(?P<pk>\d+)/$', core.views.toggle_credit_debit, name='toggle-credit-debit'),

    url(r'^transfer/user/$', core.views.create_transfer_to_user_view.new_transfer_to_user, name='transfer-user'),
    url(r'^transfer/account/$', core.views.create_transfer_to_account_view.new_transfer_to_account, name='transfer-account'),
    url(r'^transfer/bucket/$', core.views.create_transfer_to_bucket_view.CreateTransferToBucketView.as_view(), name='transfer-bucket'),

    url(r'^accounts/$', core.views.list_account_view.ListAccountView.as_view(), name='account-list'),
    url(r'^account/$', core.views.create_account_view.CreateAccountView.as_view(), name='create-account'),
    url(r'^account/(?P<pk>\d+)/$', core.views.update_account_view.UpdateAccountView.as_view(), name='update-account'),
    url(r'^inbox-account/(?P<pk>\d+)/$', core.views.update_inbox_account_view.UpdateInboxAccountView.as_view(), name='update-inbox-account'),
    url(r'^buckets/$', core.views.list_bucket_view.ListBucketView.as_view(), name='bucket-list'),
    url(r'^bucket/$', core.views.create_bucket_view.CreateBucketView.as_view(), name='create-bucket'),
    url(r'^bucket/(?P<pk>\d+)/$', core.views.update_bucket_view.UpdateBucketView.as_view(), name='update-bucket'),
    url(r'^$', RedirectView.as_view(pattern_name='dashboard'))
]
