from django.db import models
from django.conf import settings

class Task(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.author} on {self.task}'
