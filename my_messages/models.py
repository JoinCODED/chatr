from django.db import models

class Message(models.Model):
    username = models.CharField(max_length=100)
    message = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} said {self.message}'

    class Meta:
        ordering=['timestamp']
