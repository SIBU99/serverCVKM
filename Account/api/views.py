from rest_framework.generics import(
ListCreateAPIView,
RetrieveUpdateDestroyAPIView,
#RetrieveUpdateAPIView,
CreateAPIView,
#ListAPIView,
#RetrieveAPIView,
#UpdateAPIView,
#DestroyAPIView,
)
from rest_framework.permissions import(
    AllowAny,
    IsAuthenticated,
    #IsAdminUser,
    #IsAuthenticatedOrReadOnly,
    #DjangoModelPermissions,
    #DjangoModelPermissionsOrAnonReadOnly,
    #DjangoObjectPermissions
)
from json import loads
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..models import Farmer, Expert, Others, OTPTokenPhone, ExpertApply
from rest_framework.exceptions import ValidationError
from .serializer import FarmerSerializer, OthersSerializer, ExpertApplySerializer, ExpertSerializer
import requests as req
from rest_framework.parsers import (
    #JSONParser,
    FormParser,
    MultiPartParser,
    #FileUploadParser,
)


class FarmerCreate(CreateAPIView):
    "This will use to create a farmer Account"

    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [
        AllowAny,
    ]

class FarmerRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [
        AllowAny
    ]

class OthersCreate(CreateAPIView):
    queryset = Others.objects.all()
    serializer_class = OthersSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [
        AllowAny
    ]

class OthersRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Others.objects.all()
    serializer_class = OthersSerializer
    permission_classes = [
        AllowAny
    ]

class ExpertApplyListCreate(CreateAPIView):
    queryset = ExpertApply.objects.all()
    serializer_class = ExpertApplySerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [AllowAny]

class ExpertRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    permission_classes = [
        AllowAny
    ]

class GetToken(APIView):
    "this will handel the mobile number varification"
    def post(self, request, format = None):
        "this will triger when there is a post request"
        phone_number = request.data.get("phone_number", None)
        if not phone_number:
            msg = {"Error":"PLease Provide A Phone Number"}
            raise ValidationError(msg)
        print(phone_number)
        param = "vermob"
        try:
            token = OTPTokenPhone.objects.create(
                phone_number = phone_number,
                purpose = param,
            )
        except:
            try:
                token = OTPTokenPhone.objects.get(phone_number = phone_number, purpose = param)
                #! Do the Reupdate of token
            except OTPTokenPhone.DoesNotExist:
                msg = {"Error":"PLease Provide Valid Infomation"}
                raise ValidationError(msg)

        
        return Response({"Status":"Token Send"}, status = status.HTTP_201_CREATED)

class ResendTokenMobile(APIView):
    "this wil handel the resend of authentication"
    def post(self, request, format = None):
        "this will trigger when there is a post request"
        phone_number = request.data.get("phone_number", None)
        if not phone_number:
            msg = {"Error":"PLease Provide A Phone Number"}
            raise ValidationError(msg)
        param = "vermob"
        try:
            token = OTPTokenPhone.objects.get(phone_number = phone_number, purpose = param)
        except OTPTokenPhone.DoesNotExist:
            msg = {"Error":"Token Not Found"}
            raise ValidationError(msg)
        if not token.is_expired:
            token.change_request = True
            token.save()
        else:
            msg = {"Error":"Token is expired"}
            raise ValidationError(msg)

        return Response({"Status":"Send"}, status= status.HTTP_201_CREATED)

class ReupdateTokenMobile(APIView):
    "this will handel the reupdate of token"
    
    def post(self, request, format=None):
        "this will triger when post request is there"
        phone_number = request.data.get("phone_number", None)
        if not phone_number:
            msg = {"Error":"PLease Provide A Phone Number"}
            raise ValidationError(msg)
        param = "vermob"
        try:
            token = OTPTokenPhone.objects.get(phone_number = phone_number, purpose = param)
        except OTPTokenPhone.DoesNotExist:
            msg = {"Error":"Token Not Found"}
            raise ValidationError(msg)
        if token.is_reupdate:
            token.token_update = True
            token.change_request = True
            token.save()
            return Response({"Status":"send"}, status= status.HTTP_201_CREATED)
        else:
            msg = {"Error":"wait for 36 hr to activate it"}
            raise ValidationError(msg)

class VerifyToken(APIView):
    "this is to token verification of the phone number"
    
    def post(self, request, format = None):
        "this is trigger when there is a post request"
        phone_number = request.data.get("phone_number", None)
        token = request.data.get("token", None)
        if not phone_number:
            msg = {"Error": "Provide a Phone Number it is related"}
            raise ValidationError(msg)
        if not token:
            msg = {"Error":"Provide a Token to Verify"}
            raise ValidationError(msg)
        params = "vermob"
        try:
            Token = OTPTokenPhone.objects.get(
                phone_number = phone_number,
                purpose = params,
            )
        except OTPTokenPhone.DoesNotExist:
            msg = {
                "Error":"Please Provide the Valid Information Of Token"
            }
            raise ValidationError(msg)
        if Token.token == token and not(Token.is_expired):
                Token.token_used = True
                Token.save()
                return Response({"Status":"Verified"}, status = status.HTTP_202_ACCEPTED)
        else:
            return Response({"Status":"Please Provide a Valid Token"}, status = status.HTTP_406_NOT_ACCEPTABLE)

class CheckAccountPhone(APIView):
    "this will pass the phone number and return the username and full name"
    
    def post(self, request, format=None):
        "this will return the username and full name of the Farmer"
        data_dic = {
            "exists":False
        }
        phone_number = request.data.get("phone_number", None)
        if not phone_number:
            msg = "PLease Provide the Phone Number For Further Process"
            raise ValidationError(msg)
        try:
            _ = Farmer.objects.get(farmer_phone= phone_number)
            data_dic["exists"] = True
        except Farmer.DoesNotExist:
            try:
                _ = Expert.objects.get(expert_phone = phone_number)
                data_dic["exists"] = True
            except Expert.DoesNotExist:
                try:
                    _ = Others.objects.get(other_phone = phone_number)
                    data_dic["exists"] = True
                except:
                    r = req.post("http://172.29.9.89:8080/api/v1/gettoken/", data={"phone_number":phone_number})
                    if r.status_code is 201:
                        data_dic["otp"] = "send"
                    else:
                        data_dic["otp"] = "not send"
                    return Response(data_dic, status = status.HTTP_202_ACCEPTED)
        return Response(data_dic, status = status.HTTP_202_ACCEPTED) 

class LoginAccount(APIView):
    "this will check the Login API"

    def post(self, request, format=None):
        "this will trigger with post request"
        data_dic = dict()
        phone_number = request.data.get("phone_number", None)
        if not phone_number:
            msg = {"Error":"Please Provide the Valid Phone Number"}
            raise ValidationError(msg)
        password = request.data.get("password", None)
        if not password:
            msg = {"Error":"Please Provide password"}
            raise ValidationError(msg)
        
        try:
            farmer = Farmer.objects.get(farmer_phone= phone_number)
        except Farmer.DoesNotExist:
            try:
                expert = Expert.objects.get(expert_phone = phone_number)
            except Expert.DoesNotExist:
                try:
                    other = Others.objects.get(other_phone = phone_number)
                except:
                    msg = {"Error":"Please Provide a Valid Phone Number"}
                    raise ValidationError({"exists":msg})

        if farmer:
            username = farmer.farmer_user_auth.username
            r = req.post("http://172.29.9.89:8080/api/token/", data = {"username":username, "password":password})
            if r.status_code is 200:
                data_dic = loads(r.text)
                data_dic["user_id"] = farmer.farmer_id
                data_dic["type"] = "farmer"
        elif expert:
            username = expert.expert_user_auth.username
            r = req.post("http://172.29.9.89:8080/api/token/", data = {"username":username, "password":password})
            if r.status_code is 200:
                data_dic = loads(r.text)
                data_dic["user_id"] = expert.expert_id
                data_dic["type"] = "expert"
        elif other:
            username = other.other_user_auth.username
            r = req.post("http://172.29.9.89:8080/api/token/", data = {"username":username, "password":password})
            if r.status_code is 200:
                data_dic = loads(r.text)
                data_dic["user_id"] = other.other_id
                data_dic["type"] = "other"
        
        return Response(data_dic, status = status.HTTP_202_ACCEPTED)

