from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
User = get_user_model()
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateCar(request):
    
    try:
        user = request.user
        user.car_model = request.data.get("car_model")
        user.save()
        return Response({"message": "Car updated successfully"})
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateProfileImage(request):
    user = request.user

    image = request.FILES.get("image")

    if not image:
        return Response(
            {"message": "No image uploaded"},
            status=400
        )

    user.image = image
    user.save()

    return Response({
        "message": "Profile image updated successfully",
        "image": request.build_absolute_uri(user.image.url),
    })
@api_view(["GET"])
def verify(request ,uid,token):
    try:
        
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)

    except:
        return Response({"message": "Invalid user"})
  
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Email verified successfully"})
    else:
        return Response({"message": "Invalid or expired token"})
@api_view(["GET","POST"])
def reset(request ,uid,token):
    try:
        
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)

    except:
        return Response({"message": "Invalid user"})
    if not default_token_generator.check_token(user, token):
        return Response({"message": "Invalid or expired token"}, status=400)
    if request.method == "GET":
        return render(request, "reset_password.html")
    password = request.POST.get("password")
    user.set_password(password)
    user.save()
    return Response({"message": "Password changed successfully"})

    
    
@api_view(["POST"])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"})
    except Exception:
        return Response(
            {"message": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST
        )



@api_view(["POST"])
def resetPassword(request):
    email = request.data.get("email")
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
   
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = f"https://carmobile-app-backend.vercel.app/api/reset/{uid}/{token}/"
    send_mail(
            "Reset your password",
            link,
            settings.EMAIL_HOST_USER,
            [email],
        )
        
    return Response({
            "message": "Password updated",
            "name": email
        })
    
@api_view(["POST"])
def register(request):
    email = request.data.get("email")
    password = request.data.get("password")
    name = request.data.get("name")
    image = request.FILES.get("image")
    serializer = UserSerializer(data=request.data)
    print(request.data)
    print(request.FILES)
    if serializer.is_valid():
        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = f"https://carmobile-app-backend.vercel.app/api/verify/{uid}/{token}/"
        send_mail(
            "Verify your account",
            link,
            settings.EMAIL_HOST_USER,
            [email],
        )
        
        return Response({
            "message": "User oluşturuldu",
            "name": name
        })
    else:
        return Response(user.errors, status=400)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def Profile(request):
    user = request.user
    return Response({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "car_model":user.car_model,
        "image": request.build_absolute_uri(user.image.url) if user.image else None,
    })
    
        
        
     
