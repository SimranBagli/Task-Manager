from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    Role = [
            ('Manager', 'manager'),
            ('Employee', 'employee'),
            ('Client', 'client')
        ]
    role = models.CharField(
        max_length=10,
        choices=Role,
        default='Client',
    )

    def __str__(self) -> str:
        return self.username


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    task_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    create_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE, related_name='create_by')
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True,
        blank=True
        )

    def __str__(self) -> str:
        return self.title
