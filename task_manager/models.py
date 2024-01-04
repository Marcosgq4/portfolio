from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Task(models.Model):
    
    STATUS_CHOICES = (
        ('Incomplete', 'Incomplete'),
        ('Complete', 'Complete'),
    )
    
    IMPORTANCE_CHOICES = [
        ('most_important', 'Most Important'),
        ('very_important', 'Very Important'),
        ('important', 'Important'),
        ('not_important', 'Not Important'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=64)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Incomplete')
    importance = models.CharField(
        max_length=20,
        choices=IMPORTANCE_CHOICES,
        default='not_important'
    )
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'task_manager'

    def __str__(self):
        return self.title
    
