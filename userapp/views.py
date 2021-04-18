from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from userapp.serializers import UserSerializer


# Create your views here.
class RegisterView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

    def post(self,request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'access_token': token.key}, status=HTTP_200_OK)
        else:
            error =  user_serializer.errors
            return Response (error,status = HTTP_400_BAD_REQUEST)
