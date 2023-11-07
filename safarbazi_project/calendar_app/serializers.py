from rest_framework import serializers
from .models import Product, Availability

from .datetimeIR import *

class AvailabilitySerializer(serializers.ModelSerializer):
    # Use a SerializerMethodField to customize the 'date' field serialization.
    date = serializers.SerializerMethodField()

    class Meta:
        model = Availability
        # Include all fields in the serialization.
        fields = '__all__'

    def get_date(self, obj):
        # Convert the 'date' field from Gregorian to Jalali
        gregorian_date = obj.date
        jalali_date = persian_conventer(gregorian_date) 
        jalali_date_str = jdatetime.datetime.strftime(jalali_date, '%Y-%m-%d')
        return jalali_date_str

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        # Include all fields in the serialization.
        fields = '__all__'

    