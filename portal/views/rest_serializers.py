from django.http import response, Http404
from rest_framework import routers, serializers, permissions, status, generics
from rest_framework.views import APIView
import django_filters.rest_framework
from custom.models import Invoice, VwInvoiceDetailAzureAzure, Organization, InvoiceTable
from custom.services import get_organization
from rest_framework.response import Response

class InvoiceTableSerializer(serializers.ModelSerializer):
    orgid = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), style={'base_template': 'input.html'})
    class Meta:
        model = InvoiceTable
        fields = '__all__'
        read_only_fields = (
            "seq",
            "invoicemonth",
            # "invoicedate",
            # "invoiceid",
            # "orgid",
            "orgkey",
            "vendorcode",
            "vendorinvoicecount",
            # "chargestartdate",
            # "chargeenddate",
            "partner_amount_pretax",
            "rrp_amount_pretax",
            "our_amount_pretax",
            "our_tax",
            "our_amount",
            # "regid",
            "regdate",
            # "statecode",
            "statechgid",
            "statechgdate",
            # "remark"
        )

# Serializers define the API representation.
class InvoiceSerializer(serializers.ModelSerializer):
    orgId = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), style={'base_template': 'input.html'})
    class Meta:
        model = Invoice
        read_only_fields = (
            "seq",
            # "invoiceMonth",
            "invoiceId",
            "orgKey",
            "orgName",
            "vendorCode",
            "vendorName",
            "vendorInvoiceCount",
            "partnerAmount",
            "rrpAmount",
            "ourAmount",
            "paid",
            "regDate",
            "statechgid",
            "statechgdate",
        )
        fields = '__all__' 
        # fields = ['url', 'username', 'email', 'is_staff']

# Serializers define the API representation.
class InvoiceDetailAzAzSerializer(serializers.ModelSerializer):
    orgid = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), style={'base_template': 'input.html'})
    class Meta:
        model = VwInvoiceDetailAzureAzure
        fields = '__all__' 
        # fields = ['url', 'username', 'email', 'is_staff']