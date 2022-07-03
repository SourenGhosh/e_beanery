
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException, ValidationError

from rest_framework import generics
from rest_framework import mixins


from base.serializers import OrderSerializers, TableSerializer, BillingDetailSerializers

from base.models import Order, UserSetting, Table
from .tasks import async_bill_generation


class ViewOrder(APIView):
    permissions_class = [IsAuthenticated]
    
    @swagger_auto_schema(responses={200: OrderSerializers(many=True)})
    def get(self, request, *args, **kwargs):
        qs = Order.objects.all()
        user = request.user.user_setting
        print("user first name", user)
        if user.user_type == UserSetting.USER_CHOICES[0][0]:
            qs = qs.filter(customer=user)
        serializers = OrderSerializers(qs, many=True)
        return Response(
            serializers.data,
            status = status.HTTP_200_OK
        )

    @swagger_auto_schema(responses={200: OrderSerializers(many=True)}, request_body = OrderSerializers)
    def post(self, request, *args, **kwargs):
        data = request.data
        serializers = OrderSerializers(data = data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(
            serializers.data,
            status = status.HTTP_201_CREATED
        )
    @swagger_auto_schema(
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT, 
        properties={
            'order_id': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        }
    ))
    @permission_required('order.can_change_status')
    def put(self, request, *args, **kwargs):
        status = request.data.get('status')
        order = Order.objects.get(id = request.data.get('order_id'))
        order.status = status
        order.save()
        if status == Order.order_status[2][0]:
            async_bill_generation.delay(order)
            
            
        return Response(
            status  = status.HTTP_201_CREATED
        )
            


class ViewTable(APIView):
    def get(self, *args, **kwargs):
        qs = Table.objects.filter(is_booked=False)
        serializers = TableSerializer(qs, many=True)
        return Response(
            serializers.data,
            status = status.HTTP_200_OK
        )
        
class BillingDetails(APIView):
    def get(self, request):
        qs = BillingDetailSerializers.objects.all()
        serializers = BillingDetailSerializers(qs, many=True)
        return Response(
            serializers.data,
            status = HTTP_200_OK
        )
    def post(self, request):
        data = request.data
        serializers = BillingDetailSerializers(data = data)
        serializers.is_valid(raise_exception = True)
        serializers.save()
        return Response(
            serializers.data,
            status = status.HTTP_200_OK
        )




def index(request):
    return render(request, "base/index.html")