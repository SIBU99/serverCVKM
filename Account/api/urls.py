from django.urls import path
from .views import (
    FarmerCreate,
    FarmerRetrieveUpdateDestroyView,
    CheckAccountPhone,
    LoginAccount,
    GetToken,
    ResendTokenMobile,
    ReupdateTokenMobile,
    VerifyToken,
    OthersCreate,
    OthersRetrieveUpdateDestroyView,
    ExpertApplyListCreate,
    ExpertRetrieveUpdateDestroyView
)
urlpatterns = [
    path("Farmers/", FarmerCreate.as_view(), name="Farmer-list"),
    path("Farmers/<slug:pk>/", FarmerRetrieveUpdateDestroyView.as_view(), name="Farmer-detail"),
    path("Others/", OthersCreate.as_view(), name="Other-view"),
    path("Others/<int:pk>/",OthersRetrieveUpdateDestroyView.as_view(), name="Other-detail"),
    path("expertapply/", ExpertApplyListCreate.as_view(), name="expert-apply-create"),
    path("experts/<slug:pk>/", ExpertRetrieveUpdateDestroyView.as_view(), name="expert-details"),
    path("checkphonenumber/", CheckAccountPhone.as_view(), name="Check_Phone-datail"),
    path("alllogin/", LoginAccount.as_view(), name="login-auth-user"),
    path("gettoken/", GetToken.as_view(), name="send-token"),
    path("resendtoken/", ResendTokenMobile.as_view(), name="resend-token"),
    path("regeneratetoken/", ReupdateTokenMobile.as_view(), name="reupdate_token"),
    path("verifytoken/", VerifyToken.as_view(), name="verify-token"),
]
