from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={
                                         'input_type': 'password',
                                         'placeholder': 'password'
                                     })

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={
                                         'input_type': 'password',
                                         'placeholder': 'password'
                                     })


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=128)
    content = serializers.CharField(style={'base_template': 'textarea.html'})

    class Meta:
        model = Post
        fields = ['title', 'content']


class PostListSerializer(serializers.ModelSerializer):
    user_like_dislike = serializers.CharField(write_only=True)

    class Meta:
        model = Post
        fields = "__all__"
