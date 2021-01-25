from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import AuthSerializer, UserSerializer
from .models import User


class UserViewSet(viewsets.ViewSet):
    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(methods=['POST'],
            detail=False,
            permission_classes=[AllowAny])
    def login(self, request):
        serializer = AuthSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=400
            )

        user, is_new_user = User.objects.get_or_create(
            username=serializer.data['username']
        )

        if is_new_user:
            user.set_password(serializer.data['password'])
            user.save(update_fields=['password'])
        elif not user.check_password(serializer.data['password']):
            return Response(
                {'error': "Invalid username or password"},
                status=400
            )

        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'user': UserSerializer(user).data,
            'token': token.key
        }
        return Response(
            data=data,
            status=201 if is_new_user else 200
        )
