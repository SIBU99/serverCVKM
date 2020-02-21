from django.urls import path
from .views import SeedlingDetect

urlpatterns = [
    path("seedlind/", SeedlingDetect.as_view(), name="Seedling")
]

