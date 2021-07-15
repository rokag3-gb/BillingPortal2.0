from django.http import response, Http404
from rest_framework import routers, permissions, status, generics
from rest_framework.views import APIView
from django_filters import rest_framework as drf_filters
from custom.models import Invoice, InvoiceTable, VwInvoiceDetailAzureAzure, Organization
from custom.services import get_organization
from rest_framework.response import Response
from .rest_serializers import InvoiceDetailAzAzSerializer, InvoiceSerializer, InvoiceTableSerializer
from drf_yasg.views import get_schema_view
from drf_yasg import openapi    
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework.decorators import action, api_view

swagger_view = get_schema_view(
   openapi.Info(
      title="MateBilling Invoice REST API",
      default_version='v1',
      description="MateBilling Invoice REST API"
   ),
   public=True,
   permission_classes=[permissions.IsAuthenticated],
)

class InvoiceFilter(drf_filters.FilterSet):
    invoiceDate = drf_filters.DateFromToRangeFilter(field_name='invoiceDate')
    class Meta:
        model = Invoice
        fields = ['invoiceMonth', 'invoiceDate', 'orgId', 'orgKey', 'orgName', 'vendorCode', 'vendorName']

@swagger_auto_schema(method='get', responses={200: InvoiceTableSerializer()})
@action(detail=False, methods=['get'])
class InvoiceRestList(generics.ListAPIView):
    model = Invoice
    serializer_class = InvoiceSerializer
    filter_backends = [drf_filters.DjangoFilterBackend]
    filterset_class = InvoiceFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Invoice.objects.filter(orgid=get_organization(self.request))
        return Invoice.objects.all()
class InvoiceRestCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(method='post', request_body=InvoiceTableSerializer, responses={200: InvoiceTableSerializer()})
    @action(detail=False, methods=['post'])
    def post(self, request, format=None):
        if request.user.is_staff:
            serializer = InvoiceTableSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404
class InvoiceRestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, request, pk):
        try:
            if(request.user.is_staff):
                return Invoice.objects.get(pk=pk)
            else:
                return Invoice.objects.get(pk=pk, orgId=get_organization(request))
        except Invoice.DoesNotExist:
            raise Http404
    
    def get_tblrow_object(self, request, pk):
        try:
            if(request.user.is_staff):
                return InvoiceTable.objects.get(pk=pk)
            else:
                return InvoiceTable.objects.get(pk=pk, orgId=get_organization(request))
        except Invoice.DoesNotExist:
            raise Http404

    @swagger_auto_schema(method='get', responses={200: InvoiceSerializer()})
    @action(detail=True, methods=['get'])
    def get(self, request, pk: int, format=None):
        snippet = self.get_object(request, pk)
        serializer = InvoiceSerializer(snippet)
        return Response(serializer.data)

    @swagger_auto_schema(method='put', request_body=InvoiceTableSerializer, responses={200: InvoiceTableSerializer()})
    @action(detail=True, methods=['put'])
    def put(self, request, pk: int, format=None):
        if request.user.is_staff:
            snippet = self.get_tblrow_object(request, pk)
            serializer = InvoiceTableSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404

    @swagger_auto_schema(method='delete')
    @action(detail=True, methods=['delete'])
    def delete(self, request, pk: int, format=None):
        if request.user.is_staff:
            snippet = self.get_tblrow_object(request, pk)
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404

class InvoiceDetailAzAzRestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, request, pk):
        try:
            if(request.user.is_staff):
                return VwInvoiceDetailAzureAzure.objects.get(pk=pk)
            else:
                return VwInvoiceDetailAzureAzure.objects.get(pk=pk, orgid=get_organization(request))
        except VwInvoiceDetailAzureAzure.DoesNotExist:
            raise Http404

    def get(self, request, pk: int, format=None):
        snippet = self.get_object(request, pk)
        serializer = InvoiceDetailAzAzSerializer(snippet)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if request.user.is_staff:
            serializer = InvoiceDetailAzAzSerializer(data=request.data)
            if serializer.is_valid():
                serializer.create()
                return response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404

    def put(self, request, pk: int, format=None):
        if request.user.is_staff:
            snippet = self.get_object(request, pk)
            serializer = InvoiceDetailAzAzSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404

    def delete(self, request, pk: int, format=None):
        if request.user.is_staff:
            snippet = self.get_object(request, pk)
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise Http404

class InvoiceDetailAzAzRestList(generics.ListAPIView):
    model = VwInvoiceDetailAzureAzure
    serializer_class = InvoiceDetailAzAzSerializer
    filter_backends = [drf_filters.DjangoFilterBackend]
    filterset_fields = ['invoicemonth', 'invoicedate', 'invoiceid', 'orgid', 'orgname', 'orgkey', 'vendorcode', 'vendorname']
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if not self.request.user.is_staff:
            return VwInvoiceDetailAzureAzure.objects.filter(orgid=get_organization(self.request))
        return VwInvoiceDetailAzureAzure.objects.all()

    