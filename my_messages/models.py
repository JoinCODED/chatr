from django.db import models

class Message(models.Model):
    username = models.CharField(max_length=100)
    message = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-timestamp']
