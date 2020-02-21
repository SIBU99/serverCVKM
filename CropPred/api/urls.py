from django.url import path 
from .views import CropPrediction

urlpatterns = [
    path("corn-predict/", CropPrediction.as_view(), name = "Corp_Predict"),
]
