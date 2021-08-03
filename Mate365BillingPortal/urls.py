"""Mate365BillingPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from portal.views.payment_token import cert_form
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import path, include
from organizations.backends import invitation_backend

from custom.views import CustomLoginView
from portal.views import payment, dashboard, index, preference, invoices, charge_oneimte_payment, \
    payment_history, payment_details, manage_payments, search_orgs, orgsettings, \
    cert_form, issue_token, issue_param, issue_param_callback, charge_token_payment, invoice_backoffice_iframe, \
    invoice_list_iframe
from portal.views.invoice_backoffice import InvoiceCreateListView, InvoiceRestView, InvoiceDetailAzAzCreateListView, \
    InvoiceDetailAzureRestListView, swagger_view, get_invoice_report
from django.conf import settings # import the settings file

branding = getattr(settings, "BRANDING", {})
admin.site.site_header = "{} BackOffice".format(branding["NAME"])
admin.site.site_title = "{} BackOffice UI".format(branding["NAME"])
admin.site.index_title = "{} BackOffice 접속을 환영합니다".format(branding["NAME"])

urlpatterns = [
    path('hq/login/', LoginView.as_view(template_name="registration/login.html", ), name='login'),
    path('hq/', admin.site.urls),

    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/', include('django.contrib.auth.urls')),

    path('organization/', include('custom.urls')),
    path('powerbi/', include('powerbi.urls')),

    path('payment/', login_required(payment), name='payment'),
    path('payment/charge/onetime', login_required(charge_oneimte_payment), name='charge_onetime'),
    path('payment/charge/withtoken', login_required(charge_token_payment), name="charge_with_token"),

    path('invoices/', login_required(invoices), name='invoices'),
    path('payment_history/', login_required(payment_history), name='payment_history'),
    path('payment_details/', login_required(payment_details), name='payment_details'),
    path('search_orgs/', login_required(search_orgs), name='search_orgs'),
    path('invoice_list/', login_required(invoice_list_iframe), name='invoice_list'),
    path('invoice_backoffice/', login_required(invoice_backoffice_iframe), name='invoice_backoffice'),

    path('manage_payments/', login_required(manage_payments), name="manage_payments"),
    path('manage_payments/new/', login_required(cert_form), name="new_payment"),
    path('manage_payments/issue_param/', login_required(issue_param), name="issue_param"),
    path('manage_payments/issue_param/callback/', issue_param_callback, name="issue_param_callback"),

    path('manage_payments/issue_token/', login_required(issue_token), name="issue_token"),

    path("invite/", include(invitation_backend().get_urls())),

    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('settings/', preference, name='settings'),
    path('settings/org/', orgsettings, name='orgsettings'),
    path('settings/org/', orgsettings, name='organization_list'),

    path('policy/', include('policy.urls')),
    path('api/v1/invoice/', InvoiceCreateListView.as_view()),
    path('api/v1/invoice/<int:pk>/', InvoiceRestView.as_view()),
    path('api/v1/invoice/detail/azure/', InvoiceDetailAzAzCreateListView.as_view()),
    path('api/v1/invoice/detail/azure/<str:invoice_id>', InvoiceDetailAzureRestListView.as_view()),
    path('api/v1/invoice_report/<str:invoice_id>/', get_invoice_report),
    path('api-auth/', include('rest_framework.urls')),
    path('swagger/schema-json.json', swagger_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', swagger_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('app/', include('invoice_backoffice.urls')),
    path('', index, name='index'),
]
