from rest_framework.views import APIView
from rest_framework.permissions import(
    AllowAny,
    #IsAuthenticated,
    #IsAdminUser,
    #IsAuthenticatedOrReadOnly,
    #DjangoModelPermissions,
    #DjangoModelPermissionsOrAnonReadOnly,
    #DjangoObjectPermissions
)
from rest_framework.parsers import (
    #JSONParser,
    FormParser,
    MultiPartParser,
    #FileUploadParser,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from Seedling.Seedling import predict

class SeedlingDetect(APIView):
    def post(sef, request, format =None):
        img = request.data.get(img,None)
        if not img:
            raise ValidationError(
                {
                    "Error":"PLease Provide Image"
                }
            )
        result = predict(img)

        return Response(
            result,
            status = status.HTTP_201_CREATED
        )
        