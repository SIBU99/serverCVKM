from rest_framework import serializers
from ..models import PostIng, Reply, Comment
from rest_framework.exceptions import ValidationError
from Account.models import (
    Farmer,
    Expert,
    Others,
)
from rest_framework.exceptions import ValidationError

class FarmerHelperSerializer(serializers.ModelSerializer):
    "This the serializer for the model : Farmer"
    class Meta:
        model = Farmer
        fields = [
            "farmer_id",
            "farmer_full_name",
            "farmer_dp",
        ]
        extra_kwargs = {
            "farmer_full_name":{
                "required":False
            }
        }

class ExpertHelperSerializer(serializers.ModelSerializer):
    "This the serializer for the model : Expert"
    class Meta:
        model = Expert
        fields = [
            "expert_id",
            "expert_full_name",
            "expert_dp"
        ]
        extra_kwargs = {
            "expert_full_name":{
                "required":False
            }
        }

class OthersHelperSerializer(serializers.ModelSerializer):
    "This the serializer for the model : Others"
    class Meta:
        model = Others
        fields = [
            "id",
            "other_full_name",
            "other_dp"
        ]
        extra_kwargs = {
            "other_full_name":{
                "required":False
            }
        }


class ReplyHelperSerializer(serializers.ModelSerializer):
   "This the serializer for the model : Reply"
   class Meta:
        model = Reply
        fields = [
            "id",
            "name",
            "description",
        ]

class CommentHelperSerializer(serializers.ModelSerializer):
   "This the serializer for the model : Comment"
   class Meta:
        model = Comment
        fields = [
            "id"
            "name",
            "description"
        ]


class PostIngSerializer(serializers.ModelSerializer):
    "This the serializer for the model : PostIng"
    farmer = FarmerHelperSerializer(required=False)
    expert = ExpertHelperSerializer(required=False)
    other =  OthersHelperSerializer(required=False)
    comments = CommentHelperSerializer(many = True, read_only = True)
    class Meta:
        model = PostIng
        fields = [
            "post_id",
            "tags",
            "description",
            "farmer",
            "expert",
            "other",
            "when",
            "img_url",
            "img",
            "tags_separated",
            "comments", # this will added with comment
            "name",
        ]
        depth = 1

class PostIngHelperSerializer(serializers.ModelSerializer):
   "This the serializer for the model : PostIng"
   class Meta:
        model = PostIng
        fields = [
            "post_id",
            "tags",
            "description"
        ]

class CommentSerializer(serializers.ModelSerializer):
    "This Commenterializer for the model : model"
    farmer = FarmerHelperSerializer()
    expert = ExpertHelperSerializer()
    other  = OthersHelperSerializer()
    post = PostIngHelperSerializer()
    class Meta:
        model = Comment
        fields = [
            "comment_id",
            "farmer",
            "expert",
            "other",
            "post",
            "description",
            "tags",
            "when",
            "img_url",
            "img",
        ]
    
    depth = 1

class CommentHelperSerializer(serializers.ModelSerializer):
   "This the serializer for the model : Comment"
   class Meta:
        model = Comment
        fields = [
            "comment_id",
            "description",
            "tags",
        ]



class ReplySerializer(serializers.ModelSerializer):
    "This the serializer for the model : Reply"
    comment = CommentHelperSerializer()
    farmer = FarmerHelperSerializer()
    expert = ExpertHelperSerializer()
    other = OthersHelperSerializer()
    
    class Meta:
        model = Reply
        fields = [
            "id",
            "farmer",
            "expert",
            "other",
            "comment",
            "description",
            "when",
            "img_url",
            "img",
            "name",
        ]
        read_only_fields = [
            "when",
        ]
    depth = 1

