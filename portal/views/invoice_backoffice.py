from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from custom.models import Invoice, VwInvoiceDetailAzureAzure

# Serializers define the API representation.
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__' 
        # fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

# Serializers define the API representation.
class InvoiceDetailAzAzSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwInvoiceDetailAzureAzure
        fields = '__all__' 
        # fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class InvoiceDetailAzAzViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceDetailAzAzSerializer

# Routers provide an easy way of automatically determining the URL conf.
rest_router = routers.DefaultRouter()

rest_router.register('invoice_master', InvoiceViewSet)
rest_router.register('invoice_azaz', InvoiceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]