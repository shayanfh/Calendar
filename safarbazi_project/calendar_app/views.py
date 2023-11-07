import datetime

from django.shortcuts import render
from rest_framework import views,viewsets, status
from rest_framework.response import Response
from .models import Product, Availability
from .serializers import ProductSerializer, AvailabilitySerializer
from .authentication import StaticTokenAuthentication

from .datetimeIR import *
# Create your views here.

# Define a viewset that uses Token Authentication for Models.
class TokenAuthenticationViewSet(viewsets.ModelViewSet):
    authentication_classes = [StaticTokenAuthentication]

# Define an API view that uses Token Authentication for search api.
class TokenAuthenticationAPIView(views.APIView):
    authentication_classes = [StaticTokenAuthentication]

# Define a viewset for Product model using Token Authentication.
class ProductViewSet(TokenAuthenticationViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Override the destroy method to handle deletion
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# Define a viewset for Availability model using Token Authentication.
class AvailabilityViewSet(TokenAuthenticationViewSet):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    # Create method for adding availability entries.
    def create(self, request, *args, **kwargs):
        data = request.data
        product_id = data.get('product')

        if not product_id:
            return Response({"error": "Product ID is required in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the date field contains a single date or a date range
        date = data.get('date')
        date_range = data.get('date_range')

        if date:
            date = jdatetime.datetime.strptime(date, '%Y-%m-%d')
            date = gregorian_converter(date)

            # Check if an Availability entry with the same date and product_id already exists
            if Availability.objects.filter(product_id=product_id, date=date).exists():
                return Response({"error": "Availability with the same date and product already exists."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a single availability entry for a specific date
            Availability.objects.create(product_id=product_id, date=date, price=data.get('price'), available=data.get('available'))
        elif date_range:
            # Create multiple availability entries for a date range
            start_date = jdatetime.datetime.strptime(date_range.get('start_date'), '%Y-%m-%d')
            start_date = gregorian_converter(start_date)
            end_date = jdatetime.datetime.strptime(date_range.get('end_date'), '%Y-%m-%d')
            end_date = gregorian_converter(end_date)

            # Check if an Availability entry with the same date and product_id already exists for each date in the range
            if Availability.objects.filter(product_id=product_id, date=start_date).exists():
                return Response({"error": "Availability with the same date for the product already exists."}, status=status.HTTP_400_BAD_REQUEST)

            # Generate availability entries for each date in the range
            while start_date <= end_date:
                Availability.objects.create(product_id=product_id, date=start_date, price=data.get('price'), available=data.get('available'))
                start_date += datetime.timedelta(days=1)
        else:
            return Response({"error": "Either 'date' or 'date_range' is required in the request data."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Availability added successfully."}, status=status.HTTP_201_CREATED)

    # Override the destroy method to handle availability deletion.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Availability deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

# Define a view for searching available products and calculating the total price.
class SearchView(TokenAuthenticationAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        start_date = jdatetime.datetime.strptime(data['start_date'], '%Y-%m-%d')
        start_date = gregorian_converter(start_date)
        end_date = jdatetime.datetime.strptime(data['end_date'], '%Y-%m-%d')
        end_date = gregorian_converter(end_date)
        adult_count = data['adult_count']
        child_count = data.get('child_count',0)
        infant_count = data.get('infant_count',0)

        # Filter available products based on date range and availability.
        available_products = Product.objects.filter(
            availability__date__range=(start_date, end_date),
            availability__available=True
        ).distinct()

        # print(Product.objects.all())
        # print(Availability.objects.all())

        result = []

        for product in available_products:
            availability_objects = Availability.objects.filter(
                product=product,
                date__range=(start_date, end_date),
                available=True
            )
            
            total_price = 0
            nights = len(availability_objects)-1

            for availability in availability_objects:
                if availability != availability_objects.last():
                    total_price += availability.price

            # If the adult count is begger than standard capacity, calculate the guests price
            guest_count = adult_count-product.standard_capacity
            if guest_count > 0:
                total_price += (product.adult_price * guest_count * nights)

            # Calculate the children price
            total_price += (product.child_price * child_count * nights)
            # Calculate the Infants price
            total_price += (product.infant_price * infant_count * nights)

            result.append({
                "product_name": product.name,
                "price": total_price,
            })

        return Response(result, status=status.HTTP_200_OK)