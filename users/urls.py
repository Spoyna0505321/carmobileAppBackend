from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import logout, updateProfileImage,register, verify,resetPassword,reset, Profile,updateCar,MyTokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path("reset_password/", resetPassword),
    path("register/", register),
    path("verify/<uid>/<token>/", verify),
    path("reset/<uid>/<token>/", reset),
    path("logout/", logout),
    path("login/", MyTokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("profile/",Profile),
    path("car/",updateCar),
    path("updateImage/",updateProfileImage),
]