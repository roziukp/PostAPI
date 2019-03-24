from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib import auth
from .serializers import (TokenSerializer, PostSerializer, PostListSerializer)
from .models import Post
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserRegistration(generics.CreateAPIView):
    """
        User registration api view
        POST register/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        email = request.data.get('email', '')

        try:
            valid_email = validate_email(email)
        except ValidationError:
            return Response(
                data={
                    'message': 'Enter proper e-mail address!'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if username and password:
            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=valid_email
            )
            return Response(
                data={
                    'message': 'User {}, was created successfully!'.format(new_user.username),
                },
                status=status.HTTP_201_CREATED)

        return Response(
            data={
                'message': 'Fields: username, password and email are required! Check each field!'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLogin(generics.CreateAPIView):
    """
    POST login/
    """
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return Response({
                "token": jwt_encode_handler(jwt_payload_handler(user)),
                'username': username,
            }, status=200)
        return Response(
            data={
                'message': 'Could not authorize user with this credentials! Check each field!'
            },
            status=status.HTTP_401_UNAUTHORIZED)


class PostListView(generics.ListAPIView):
    """
         GET post_list/
    """

    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.AllowAny,)


class PostCreateView(generics.CreateAPIView):
    """
         POST post_create/
    """
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class Likes(APIView):
    """
         GET post/<pk>/like
    """
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request, pk):
        post = Post.objects.get(pk=pk)
        if request.user not in post.user_like_dislike.all():
            post.user_like_dislike.add(request.user)
            post.add_likes()
            return Response(
                data={
                    'message': 'Like was added successfully!',
                    'title': post.title,
                    'content': post.content,
                    'likes': post.likes,
                    'created_by': post.created_by.username,
                },
                status=status.HTTP_200_OK)

        return Response(
            data={
                'message': 'Like for this post is already added by this user!'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class Unlike(APIView):
    """
         GET post/<pk>/dislike
    """
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request, pk):
        post = Post.objects.get(pk=pk)
        if request.user in post.user_like_dislike.all():
            post.user_like_dislike.remove(request.user)
            post.add_dislikes()
            return Response(
                data={
                    'message': 'Post was successfully disliked!',
                    'title': post.title,
                    'content': post.content,
                    'likes': post.likes,
                    'created_by': post.created_by.username,
                },
                status=status.HTTP_200_OK)

        return Response(
            data={
                'message': 'Post has not any like provided by this user'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
