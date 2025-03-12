# from rest_framework import serializers
# from django.contrib.auth.models import User

# from .models import Task

# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'password']

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)  # Securely hashes password
#         return user

# tasks/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Comment

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'parent', 'author', 'created_date', 'replies']
        read_only_fields = ['author', 'created_date', 'replies']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'owner', 'comments']
        read_only_fields = ['owner', 'comments']

# User Registration Serializer
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password", style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
