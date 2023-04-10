from django.contrib.auth.models import Group, User
from rest_framework import serializers
from django_api.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "description"]


class PostListSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField(read_only=True)

    def get_author_username(self, obj: Post) -> str:
        try:
            return obj.author.username
        except Exception as error:
            return ""

    class Meta:
        model = Post
        exclude = ["author"]


class PostUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=300)
    description = serializers.CharField(max_length=3000)
    is_completed = serializers.BooleanField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']  #


class UserDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):  # HyperlinkedModelSerializer
    class Meta:
        model = Group
        fields = '__all__'

