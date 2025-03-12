from django.urls import path
from .views import TaskListCreateView, TaskUpdateView, CommentCreateView, CommentUpdateView


urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),
]