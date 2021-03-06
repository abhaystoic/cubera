from django.conf.urls import patterns, include, url
from django.contrib import admin
from securest import views

urlpatterns = patterns('',
    url(r'^signup$', views.sign_up, name='sign_up'),
    url(r'^signin$', views.sign_in, name='sign_in'),
    url(r'^get_merchants', views.get_merchants, name='get_merchants'),
    url(r'^notify_nearby_merchants', views.notify_nearby_merchants, name='notify_nearby_merchants'),
    url(r'^accept_request', views.accept_request, name='accept_request'),
    url(r'^get_merchants', views.get_merchants, name='get_merchants'),
    url(r'^select_merchant', views.select_merchant, name='select_merchant'),
    url(r'^verify_otp', views.verify_otp, name='verify_otp'),
    url(r'^rate_merchant', views.rate_merchant, name='rate_merchant'),
    url(r'^debit', views.debit, name='debit'),
    url(r'^credit', views.credit, name='credit'),
)
