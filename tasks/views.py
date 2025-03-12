
from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer, UserRegisterSerializer
from .permissions import IsOwnerOrReadOnlyTask, IsAuthorOrReadOnlyComment

# Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

# Task Endpoints

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # return Task.objects.filter(owner=self.request.user)
        return Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyTask]

# Comment Endpoints

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Saves a new comment instance with the current user as the author and the specified task.

        Parameters:
        serializer (CommentSerializer): The serializer instance containing the validated data for the comment.

        Raises:
        serializers.ValidationError: If the 'task' field is missing from the request data or if the specified task does not exist.

        Returns:
        None: The function does not return a value. It saves the comment instance to the database.
        """
        task_id = self.request.data.get("task")  # Get task_id from request
        if not task_id:
            raise serializers.ValidationError({"task": "This field is required."})

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise serializers.ValidationError({"task": "Task not found."})

        serializer.save(author=self.request.user, task=task)  # Ensure task is assigned


class CommentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnlyComment]

