from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import logout, register, verify, MyTokenObtainPairView

urlpatterns = [
    path("register/", register),
    path("verify/<uid>/<token>/", verify),
    path("logout/", logout),
    path("login/", MyTokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]