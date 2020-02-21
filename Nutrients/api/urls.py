from django.urls import path
from .views import NutrientExamination

urlpatterns = [
    path("nutrient-examination/", NutrientExamination.as_view(), name="nutrient-examination"),
]
