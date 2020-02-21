from django.urls import path
from .views import (
    ReplyList,
    ReplyListCreate,
    ReplyRetrieveUpdateDestroyView,
    ReplyCreateCheck,
    CommentList,
    CommentListCreate,
    CommentCreateCheck,
    CommentRetrieveUpdateDestroyView,
    PostIngCreate,
    #PostIngCreateCheck,
    PostIngList,
    PostIngRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("posts/create/", PostIngCreate.as_view(), name="post-create"),
    #path("post/check/",PostIngCreateCheck.as_view(), name="post-check"),
    path("posts/<slug:pk>/", PostIngRetrieveUpdateDestroyView.as_view(), name="post-datail"),
    path("post/", PostIngList.as_view(), name="post-list"),
    path("replies/create/", ReplyListCreate.as_view(), name="reply-create"),
    path("replies/check/", ReplyCreateCheck.as_view(), name="reply-check"),
    path("replies/<int:pk>/", ReplyRetrieveUpdateDestroyView.as_view(), name="reply-detail"),
    path("replies/", ReplyList.as_view(), name="reply-list" ),
    path("comments/create/", CommentListCreate.as_view(), name="comment-create"),
    path("comments/check/",CommentCreateCheck.as_view(), name="comment-check" ),
    path("comments/<int:pk>/", CommentRetrieveUpdateDestroyView.as_view(), name="comment-datail"),
    path("comments/", CommentList.as_view(), name="comment-list"),
]
