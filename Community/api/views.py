from rest_framework.generics import(
#ListCreateAPIView,
RetrieveUpdateDestroyAPIView,
#RetrieveUpdateAPIView,
CreateAPIView,
ListAPIView,
#RetrieveAPIView,
#UpdateAPIView,
#DestroyAPIView,
)
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import (
    #JSONParser,
    FormParser,
    MultiPartParser,
    #FileUploadParser,
)
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
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
from .serializers import(
    PostIngSerializer,
    CommentSerializer,
    ReplySerializer
)
from ..models import (
    Reply,
    Comment,
    PostIng
)
from Account.models import Farmer,Expert,Others
from django.db.models import Q

class PostIngCreate(APIView):
    parser_classes = (
        FormParser,
        MultiPartParser,
    )
    def post(self, request, format=None):
        "this will run ever the post is called"
        print(request.data)
        farmer = request.data.get("farmer_id", None)
        expert = request.data.get("expert_id", None)
        other = request.data.get("other_id", None)
        acc , acc_type = None, None

        tags = request.data.get("tags", None)
        if not tags:
            msg = {"Error":"Please Provide the Tags"}
            raise ValidationError(msg)
        description = request.data.get("description", None)
        if not description:
            msg = {"Error":"Please Provide the Description"}
        img = request.data.get("img", None)
        img_url = request.data.get("img_url", None)
        
        if farmer:
            try:
                acc = Farmer.objects.get(farmer_id = farmer)
                acc_type = "Farmer"
            except:
                msg = "Please Provide the Valid Farmer ID"
                raise ValidationError(msg)
        elif expert:
            try:
                acc = Expert.objects.get(expert_id = expert)
                acc_type = "Expert"
            except:
                msg = "Please Provide the Valid Expert ID"
                raise ValidationError(msg)
        elif other:
            try:
                acc = Others.objects.get(id = other)
                acc_type = "Others"
            except:
                msg = "Please Provide the Valid Others ID"
                raise ValidationError(msg)
        else:
            msg  = "Please provide any one account type"
            raise ValidationError(msg)

        try:
            if acc_type == "Farmer":
                post = PostIng.objects.create(
                tags = tags,
                description = description,
                img = img,
                img_url = img_url,
                farmer = acc,
                )
            elif acc_type == "Expert":
                post = PostIng.objects.create(
                    tags = tags,
                    description = description,
                    img = img,
                    img_url = img_url,
                    expert = acc
                )
            elif acc_type == "Others":
                post = PostIng.objects.create(
                    tags = tags,
                    description = description,
                    img = img,
                    img_url = img_url,
                    other = acc
                )
        except:
            msg = {"Error":"Please provide valid information"}
            raise ValidationError(msg)

        serilaized = PostIngSerializer(post)
        return Response(serilaized.data, status = status.HTTP_201_CREATED)   

class CommentListCreate(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [AllowAny]

class CommentCreateCheck(APIView):
    parser_classes = (
        FormParser,
        MultiPartParser,
    )
    def post(self, request, format=None):
        "this will run ever the post is called"
        farmer = request.data.get("farmer_id", None)
        expert = request.data.get("expert_id", None)
        other = request.data.get("other_id", None)
        acc , acc_type = None, None

        post = request.data.get("post_id", None)
        if not post:
            msg = {"Error":"Please Provide the Post ID"}
            raise ValidationError(msg)
        try:
            post = PostIng.objects.get(post_id = post)
            print(post)
        except:
            msg = {"Error":"Please Provide Valid Post ID"}
            raise ValidationError(msg)

        tags = request.data.get("tags", None)
        if not tags:
            msg = {"Error":"Please Provide the Tags"}
            raise ValidationError(msg)
        description = request.data.get("description", None)
        if not description:
            msg = {"Error":"Please Provide the Description"}
        img = request.data.get("img", None)
        img_url = request.data.get("img_url", None)
        
        if farmer:
            try:
                acc = Farmer.objects.get(farmer_id = farmer)
                acc_type = "Farmer"
                print(acc)
            except:
                msg = "Please Provide the Valid Farmer ID"
                raise ValidationError(msg)
        elif expert:
            try:
                acc = Expert.objects.get(expert_id = expert)
                acc_type = "Expert"
            except:
                msg = "Please Provide the Valid Expert ID"
                raise ValidationError(msg)
        elif other:
            try:
                acc = Others.objects.get(id = other)
                acc_type = "Others"
            except:
                msg = "Please Provide the Valid Others ID"
                raise ValidationError(msg)
        else:
            msg  = "Please provide any one account type"
            raise ValidationError(msg)

        try:
            if acc_type == "Farmer":
                comment = Comment.objects.create(
                tags = tags,
                description = description,
                post = post,
                farmer = acc,
                img_url = img_url,
                img = img,
                )
            elif acc_type == "Expert":
                comment = Comment.objects.create(
                    tags = tags,
                    description = description,
                    img = img,
                    post = post,
                    img_url = img_url,
                    expert = acc
                )
            elif acc_type == "Others":
                comment = Comment.objects.create(
                    tags = tags,
                    description = description,
                    img = img,
                    post = post,
                    img_url = img_url,
                    other = acc
                )
        except:
            msg = {"Error":"Please provide valid information"}
            raise ValidationError(msg)

        serilaized = CommentSerializer(comment)

        return Response(serilaized.data, status = status.HTTP_201_CREATED)   


class ReplyListCreate(CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [AllowAny]

class ReplyCreateCheck(APIView):
    "this is to create reply"
    parser_classes = (
        FormParser,
        MultiPartParser,
    )
    def post(self, request, format = None):
        "This will trigger when there is a post request"
        print(request.data)
        farmer = request.data.get("farmer_id", None)
        expert = request.data.get("expert_id", None)
        other = request.data.get("other_id", None)
        acc , acc_type = None, None

        comment = request.data.get("comment_id", None)
        if not comment:
            msg = {"Error":"Please Provide the Comment ID"}
            raise ValidationError(msg)
        try:
            comment = Comment.objects.get(comment_id = comment)
        except:
            msg = {"Error":"Please Provide Valid Comment ID"}
            raise ValidationError(msg)

        description = request.data.get("description", None)
        if not description:
            msg = {"Error":"Please Provide the Description"}
        img = request.data.get("img", None)
        img_url = request.data.get("img_url", None)
        
        if farmer:
            try:
                acc = Farmer.objects.get(farmer_id = farmer)
                acc_type = "Farmer"
            except:
                msg = "Please Provide the Valid Farmer ID"
                raise ValidationError(msg)
        elif expert:
            try:
                acc = Expert.objects.get(expert_id = expert)
                acc_type = "Expert"
            except:
                msg = "Please Provide the Valid Expert ID"
                raise ValidationError(msg)
        elif other:
            try:
                acc = Others.objects.get(id = other)
                acc_type = "Others"
            except:
                msg = "Please Provide the Valid Others ID"
                raise ValidationError(msg)
        else:
            msg  = "Please provide any one account type"
            raise ValidationError(msg)

        #try:
        if acc_type == "Farmer":
                reply = Reply.objects.create(
                description = description,
                comment = comment,
                farmer = acc,
                img_url = img_url,
                img = img,
                )
        elif acc_type == "Expert":
                comment = Reply.objects.create(
                    comment = comment,
                    img = img,
                    description = description,
                    img_url = img_url,
                    expert = acc
                )
        elif acc_type == "Others":
                comment = Reply.objects.create(
                    comment = comment,
                    img = img,
                    description = description,
                    img_url = img_url,
                    other = acc
                )
        #except:
        #    msg = {"Error":"Please provide valid information"}
        #    raise ValidationError(msg)
        
        serializer = ReplySerializer(reply)
        return Response(serializer.data, status = status.HTTP_201_CREATED )

class PostIngRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = PostIng.objects.all()
    serializer_class = PostIngSerializer
    permission_classes = [AllowAny]

class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]


class ReplyRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [AllowAny]

class PostIngList(ListAPIView):
    queryset = PostIng.objects.all()
    serializer_class = PostIngSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = PostIng.objects.all()
        query = list()
        que = None
        tags = self.request.query_params.get('tags', None)
        farmer_id = self.request.query_params.get('farmer_id', None)
        expert_id = self.request.query_params.get('expert_id', None)
        other_id = self.request.query_params.get('other_id', None)
        if farmer_id and expert_id and other_id:
            msg = "Please Provide One Account to access"
            raise ValidationError(msg)
        if tags or farmer_id or expert_id or other_id:
            if tags:
                tags = tags.split("-")
                query = [Q(tags__contain = i) for i in tags]
                que = query.pop()
                for setter in query:
                    que &= setter
            if farmer_id:
                q = Q(farmer__farmer_id = farmer_id)
                if que:
                    q &= que
            elif expert_id:
                q = Q(expert__expert_id = expert_id)
                if que:
                    q &= que
            elif other_id:
                q = Q(other__id=other_id)
                if que:
                    q &= que
            queryset = PostIng.objects.filter(q)
        return queryset

class CommentList(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Comment.objects.all()
        query = list()
        que = None
        tags = self.request.query_params.get('tags', None)
        farmer_id = self.request.query_params.get('farmer_id', None)
        expert_id = self.request.query_params.get('expert_id', None)
        other_id = self.request.query_params.get('other_id', None)
        if farmer_id and expert_id and other_id:
            msg = "Please Provide One Account to access"
            raise ValidationError(msg)
        if tags or farmer_id or expert_id or other_id:
            if tags:
                tags = tags.split("-")
                query = [Q(tags__contain = i) for i in tags]
                que = query.pop()
                for setter in query:
                    que &= setter
            if farmer_id:
                q = Q(farmer__farmer_id = farmer_id)
                if que:
                    q &= que
            elif expert_id:
                q = Q(expert__expert_id = expert_id)
                if que:
                    q &= que
            elif other_id:
                q = Q(other__id=other_id)
                if que:
                    q &= que
            queryset = Comment.objects.filter(q)
        return queryset   

class ReplyList(ListAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Reply.objects.all()
        query = list()
        que = None
        tags = self.request.query_params.get('tags', None)
        farmer_id = self.request.query_params.get('farmer_id', None)
        expert_id = self.request.query_params.get('expert_id', None)
        other_id = self.request.query_params.get('other_id', None)
        if farmer_id and expert_id and other_id:
            msg = "Please Provide One Account to access"
            raise ValidationError(msg)
        if farmer_id or expert_id or other_id:
            if farmer_id:
                q = Q(farmer__farmer_id = farmer_id)
                if que:
                    q &= que
            elif expert_id:
                q = Q(expert__expert_id = expert_id)
                if que:
                    q &= que
            elif other_id:
                q = Q(other__id=other_id)
                if que:
                    q &= que
            queryset = Reply.objects.filter(q)
        return queryset