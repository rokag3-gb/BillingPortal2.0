from rest_framework import serializers
from custom.models import Invoice, VwInvoiceDetailAzureAzure, Organization, InvoiceTable

class InvoiceTableSerializer(serializers.ModelSerializer):
    orgId = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), style={'base_template': 'input.html'})
    class Meta:
        model = InvoiceTable
        fields = '__all__'
        read_only_fields = (
            "seq",
            # "invoiceMonth",
            # "invoiceDate",
            "invoiceId",
            # "orgId",
            "orgKey",
            "vendorCode",
            # "vendorInvoicecount",
            # "chargeStartDate",
            # "chargeEndDate",
            # "partner_amount_pretax",
            # "rrp_amount_pretax",
            # "our_amount_pretax",
            # "our_tax",
            # "our_amount",
            # "regId",
            "regDate",
            # "stateCode",
            "stateChgId",
            "stateChgDate",
            # "remark",
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
            "rrp_amount_pretax",
            "our_amount_pretax",
            "our_tax",
            "our_amount",
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
        # fields = '__all__' 
        exclude = ('invoicemonth', 'invoicedate', 'orgkey')
        # fields = ['url', 'username', 'email', 'is_staff']