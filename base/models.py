from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    priority = models.BooleanField(default=False)
    expand = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)

    #ordering by created date
    class Meta:
        ordering = ['due_date', '-priority']

    def __str__(self):
        return self.name