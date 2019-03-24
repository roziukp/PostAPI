from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    title = models.CharField(max_length=128, verbose_name='Post Title')
    content = models.TextField(verbose_name='Post content')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    likes = models.PositiveIntegerField(default=0)
    user_like_dislike = models.ManyToManyField(User, blank=True, related_name='user_like_dislikes')

    def __str__(self):
        return self.title

    def add_likes(self, amount=1):
        self.likes += amount
        return self.save()

    def add_dislikes(self, amount=1):
        self.likes -= amount
        return self.save()
