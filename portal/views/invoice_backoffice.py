import datetime
from django.http import response, Http404
from django.urls import path, include
from rest_framework import routers, serializers, viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from custom.models import Invoice, VwInvoiceDetailAzureAzure
from custom.services import get_organization

# Serializers define the API representation.
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__' 
        # fields = ['url', 'username', 'email', 'is_staff']

class InvoiceRestView(APIView):

    def get_object(self, request, pk):
        try:
            if(request.user.is_staff):
                return Invoice.objects.get(pk=pk)
            else:
                return Invoice.objects.get(pk=pk, orgId=get_organization(request))
        except Invoice.DoesNotExist:
            raise Http404
    def get_queryset(self):
        username = self.kwargs['username']
        return Invoice.objects.filter(purchaser__username=username)

    def get(self, request,  format=None):
        invoice_id = request.query_params.get('id')
        if invoice_id:
            invoice_id = int(invoice_id)
            snippet = self.get_object(request, invoice_id)
            serializer = InvoiceSerializer(snippet)
            return Response(serializer.data)
        else:
            result = Invoice.objects.all()
            if not request.user.is_staff:
                result = result.filter(orgId=get_organization(request))
            date_start = request.query_params.get('date_start')
            date_end = request.query_params.get('date_end')
            if date_start:
                date_start = datetime.datetime.strptime(date_start, "%Y-%m")
                result = result.filter(invoiceDate__gte=date_start)
            if date_end:
                date_end = datetime.datetime.strptime(date_end, "%Y-%m")
                date_end = date_end.replace(month=date_end.month + 1) - datetime.timedelta(days=1)
                result = result.filter(invoiceDate__lte=date_end)
            if date_start == None and date_end == None:
                date_end = datetime.datetime.now()
                date_start = date_end - datetime.timedelta(days=32)
                date_start = date_start.replace(day=1)
                result = result.filter(invoiceDate__gte=date_start)
                result = result.filter(invoiceDate__lte=date_end)
            result = result.order_by("-invoiceDate")
            return Response(InvoiceSerializer(result, many=True).data)
            
    
    def post(self, request, format=None):
        if request.user.is_staff:
            serializer = InvoiceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create()
                return response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404

    def put(self, request,  format=None):
        if request.user.is_staff:
            snippet = self.get_object(request, int(request.query_params.get('id')))
            serializer = InvoiceSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404

    def delete(self, request,  format=None):
        if request.user.is_staff:
            snippet = self.get_object(request, int(request.query_params.get('id')))
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404

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
# rest_router = routers.DefaultRouter()

# rest_router.register('invoice_master', InvoiceRestView.as_view())
# rest_router.register('invoice_azaz', InvoiceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
# urlpatterns = [
#     path('', include(router.urls)),
#     # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]