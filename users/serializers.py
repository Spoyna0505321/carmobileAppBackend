from rest_framework import serializers
from users.models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
      
            token = super().get_token(user)
            token["email"] = user.email

            return token
        
    def validate(self, attrs):
        data =  super().validate(attrs)
        if not self.user.is_active:
            raise serializers.ValidationError(
                "Please verify your email first."
            )
        return data
# for register user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {
        "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = Profile.objects.create(email=validated_data["email"],name=validated_data["name"],image= validated_data["image"])
        user.set_password(validated_data["password"])
        user.save()
        return user