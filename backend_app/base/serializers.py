from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError

from base.models import Order, Table, UserSetting, BillingDetails



class TableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Table
        exclude = ["is_booked", ]


class CustomerSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    class Meta:
        model = UserSetting
        fields = "__all__"


class OrderSerializers(serializers.ModelSerializer):
    meal_name = serializers.CharField(source='meal_type.name', read_only=True)
    customer_name = serializers.CharField(source='customer.user.first_name', read_only=True)
    class Meta:
        model = Order
        fields = ["id", "meal_name", "table", "customer", "meal_type", 'customer_name']
    
    
    def create(self, validated_data):
        print(validated_data)
        tables = validated_data['table']
        for table in tables:
            table.is_booked = True
            table.save()
        return super().create(validated_data)
        

class BillingDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = BillingDetails
        fields = "__all__"


