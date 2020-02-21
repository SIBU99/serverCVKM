from rest_framework.views import APIView
from rest_framework.response import Response
from rest_farmework import status
from rest_framework.parsers import (
    #JSONParser,
    FormParser,
    MultiPartParser,
    #FileUploadParser,
)
from rest_framework.exceptions import ValidationError
from ..nutrients.nutrient estimation import predict

class NutrientExamination(APIView):
    
    parser_classes = [
        FormParser,
        MultiPartParser,
    ]

    def post(self, request, format =None):
        image = request.data.get("Image", None)
        if not image:
            msg = {"Error":"Please Provide a Image"}
            raise ValidationError(msg)
        result = predict(image)
        
        return Response(result, status = status.HTTP_201_CREATED)
