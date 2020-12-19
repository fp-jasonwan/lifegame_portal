from .views import oc_portal, search_profile
from django.urls import path, include

urlpatterns = [
    path('', oc_portal, name='oc_portal'),
    path('search_profile', search_profile, name='search_profile')
]