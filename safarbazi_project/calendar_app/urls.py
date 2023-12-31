from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, AvailabilityViewSet,SearchView

# Create a router for handling CRUD operations on Product and Availability models.
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'availabilities', AvailabilityViewSet)

urlpatterns = [
    # Include the URLs generated by the router for Product and Availability.
    path('api/', include(router.urls)),
    # Define a custom search API endpoint using the SearchView.
    path('api/search/', SearchView.as_view(), name='search-api'),
]