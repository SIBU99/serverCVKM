from rest_framework import serializers
from ..models import Farmer, Expert, Others, ExpertApply, Document
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
   "This the serializer for the model : User"
   """
   This will be used as  imported section all the time
   """
   class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "is_active",
            "last_login",
        ]
        extra_kwargs = {
            "password":{
                "write_only":True
            },
            "is_active":{
                "read_only":True
            },
            "last_login":{
                "read_only":True
            }
        }

def get_count_number(data):
    "this will count the number of data given"
    if data == "farmer":
        count = Farmer.objects.count()
        count += 1
    elif data == "expert":
        count = Expert.objects.count()
        count += 1
    elif data == "other":
        count = Others.objects.count()
        count += 1 
    count = str(count)
    return count

class FarmerSerializer(serializers.ModelSerializer):
    "This the serializer for the model : Farmer"
    farmer_user_auth = UserSerializer()
    class Meta:
        model = Farmer
        fields = [
            "farmer_id",
            "farmer_user_auth",
            "farmer_full_name",
            "farmer_gender",
            "farmer_email",
            "farmer_verified_email",
            "farmer_phone",
            "farmer_verified_phone",
            "farmer_doj",
            "farmer_dp",
            "farmer_plot_no",
            "farmer_street",
            "farmer_landmark",
            "farmer_place",
            "farmer_city",
            "farmer_state",
            "farmer_country",
            "farmer_account_allowed",
            "farmer_digital_marketing_allowed",
        ]
        
        read_only_fields = [
            "farmer_verified_phone",
            "farmer_verified_email",
            "farmer_doj",
        ]

    def create(self, validated_data):
        "This will create the instance for many to many field " 
        farmer_user_auth = validated_data.pop("farmer_user_auth", None)
        if not farmer_user_auth:
            msg = "Please Provide the User Authentication Information"
            raise ValidationError(msg)
        auth_password = farmer_user_auth.pop("password", None)
        _ = farmer_user_auth.pop("username", None)
        if not auth_password:
            msg = "Please Provide the password"
            raise ValidationError(msg)
        auth_user = User.objects.create(
            username = "farmer"+get_count_number("farmer"),
        )
        auth_user.set_password(auth_password)
        auth_user.save()
        
        try:
            farmer = Farmer.objects.create(
                **validated_data,
                farmer_user_auth = auth_user,
            )
        except:
            msg = "Please Pass The Valid information to the Farmer Account"
            raise ValidationError(msg)
        
        return farmer
    
    def upadate(self, instance, validated_data):
        "This is the update or put haeader for the file"
        farmer_user_auth = validated_data.pop("farmer_user_auth", None)
        if farmer_user_auth:
            auth_user_id = farmer_user_auth.pop("id", None)
            try:
                auth_user = User.objects.get(id = auth_user_id)
            except:
                msg = "Please Provide A Valid ID"
                raise ValidationError(msg)
            auth_user_password = farmer_user_auth.pop("password", None)
            if auth_user_password:
                auth_user.set_password(auth_user_password)
            auth_user.save()
        
        instance.farmer_full_name = validated_data.pop("farmer_full_name", instance.farmer_full_name)
        instance.farmer_gender = validated_data.pop("farmer_gender" , instance.farmer_gender)
        instance.farmer_email = validated_data.pop("farmer_email", instance.farmer_email)
        instance.farmer_phone = validated_data.pop("farmer_phone" , instance.farmer_phone)
        instance.farmer_dp = validated_data.pop("farmer_dp", instance.farmer_dp)
        instance.farmer_plot_no = validated_data.pop("farmer_plot_no" , instance.farmer_plot_no)
        instance.farmer_street = validated_data.pop("farmer_street" , instance.farmer_street)
        instance.farmer_landmark = validated_data.pop("farmer_landmark", instance.farmer_landmark)
        instance.farmer_place = validated_data.pop("farmer_place", instance.farmer_place )
        instance.farmer_city = validated_data.pop("farmer_city", instance.farmer_city)
        instance.farmer_state = validated_data.pop("farmer_state", instance.farmer_state)
        instance.farmer_country = validated_data.pop("farmer_country", instance.farmer_country)

        return instance

class OthersSerializer(serializers.ModelSerializer):
    "This the serializer for the model : Others"
    other_user_auth = UserSerializer()
    class Meta:
        model = Others
        fields = [
            "id",
            "other_user_auth",
            "other_full_name",
            "other_gender",
            "other_email",
            "other_verified_email",
            "other_phone",
            "other_verified_phone",
            "other_post",
            "other_address",
            "other_dp"
            
        ]

        read_only_fields = [
            "other_verified_phone",
            "other_verified_email",
        ]

    def create(self, validated_data):
        "This will create the instance for many to many field " 
        other_user_auth = validated_data.pop("other_user_auth", None)
        if not other_user_auth:
            msg = {"Error":"Please Provide The User Authentication Information"}
            raise ValidationError(msg)
        password = other_user_auth.pop("password", None)
        _ = other_user_auth.pop("username", None)
        if not password:
            msg = {"Error":"Please Provide Password"}
            raise ValidationError(msg)
        try:
            user = User.objects.create(
                username = "Other"+get_count_number("other")
            )
            user.set_password(password)
            other = Others.objects.create(
                **validated_data,
                other_user_auth = user
            )
        except:
            msg = {"Error":"Please Provide a Valid Information"}
            raise ValidationError(msg)
        
        return other

class DocumentSerializer(serializers.ModelSerializer):
    "This the serializer for the model : Document"
    class Meta:
        model = Document
        fields = [
            "file",
            "linked",
        ]

class ExpertApplySerializer(serializers.ModelSerializer):
    "This the serializer for the model : ExpertApply"
    applicant_supported_docs = DocumentSerializer(many = True)
    class Meta:
        model = ExpertApply
        fields = [
            "applicant_id",
            "applicant_full_name",
            "applicant_gender",
            "applicant_status",
            "applicant_email",
            "applicant_phone",
            "applicant_verified_phone",
            "applicant_plot_no",
            "applicant_street",
            "applicant_landmark",
            "applicant_place",
            "applicant_city",
            "applicant_state",
            "applicant_country",
            "applicant_supported_docs",
        ]
    
    def create(self, validated_data):
        "This will create the instance for many to many field " 
        docs = validated_data.pop("applicant_supported_docs", None)
        if not docs:
            msg = {"Error":"Please Provide the Documents"}
            raise ValidationError(msg)
        expert_data = ExpertApply.objects.create(
            **validated_data
        )
        for doc in docs:
            Docu = Document.objects.create(**doc, linked=expert_data)
        
        return expert_data

class ExpertSerializer(serializers.ModelSerializer):
    "This the serializer for the model : Expert"
    expert_user_auth = UserSerializer()
    class Meta:
        model = Expert
        fields = [
            "expert_id",
            "expert_user_auth",
            "expert_full_name",
            "expert_gender",
            "expert_email",
            "expert_verified_email",
            "expert_phone",
            "expert_verified_phone",
            "expert_plot_no",
            "expert_street",
            "expert_landmark",
            "expert_place",
            "expert_city",
            "expert_state",
            "expert_country",
            "expert_dp",
            "expert_doj",
        ]

        read_only_fields = [
            "expert_verified_phone",
            "expert_verified_email",
            "expert_doj",
        ]
        

    def create(self, validated_data):
        "This will create the instance for many to many field " 
        expert_user_auth = validated_data.pop("expert_user_auth", None)
        if not expert_user_auth:
            msg = {"Error":"Please Provide Authentication detail"}
            raise ValidationError(msg)
        password = expert_user_auth.pop("password", None)
        if not password:
            msg = {
                "Error":"Please Provide The Password"
            }
            raise ValidationError(msg)
        try:
            user = User.objects.create(
                username = "expert"+get_count_number("expert")
            )
            user.set_password(password)
            expert = Expert.objects.create(
                **validated_data,
                expert_user_auth = user
            )
        except:
            msg = {
                "Error":"Please Provide the Information To Create Account"
            }
            raise ValidationError(msg)

        return expert
