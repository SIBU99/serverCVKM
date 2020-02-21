from django.urls import path
from .views import(
    Sprayer
)

urlpatterns = [
    path("sprayer/", Sprayer.as_view(), name="sprayer"),
]
