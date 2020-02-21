from django.urls import path
from .views import (
    WeedsDetect
)

urlpatterns = [
    path("sprayer/", WeedsDetect.as_view(), name="Weed Detect")
]
