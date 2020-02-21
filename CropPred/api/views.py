from rest_framework.views import APIView
from rest_farmework.response import Response
from rest_framework import status
from crop_pred.crop-prediction-pickle import predict

class CropPrediction(APIView):
    "this will predict the crop on the given data"
    def post(self, request, format = None):
        "this wil trigger when there will be a post request"
        ph_value = request.data.get("ph_value", 0.0)
        temp_val = request.data.get("temp_val", 0.0)
        humidity_val = request.data.get("humidity_val", 0.0)
        rainfall_val = request.data.get("rainfall_val", 0.0)
        moisture_val = request.data.get("moisture_val", 0.0)

        pass_list = [
            [
            ph_val, 
            temp_val,
            humidity_val, 
            rainfall_val, 
            moisture_val,
            ]
        ]
        result = predict(pass_list)

        return Response(
            {
            "Crop":result
            }, 
            status = status.HTTP_201_CREATED
        )
