from django.db import models
from django.conf import settings


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('TEXT', 'Text Update'),
        ('IMAGE', 'Photo / Gallery'),
        ('VIDEO', 'Video Highlight'),
        ('ARTICLE', 'Article / Report'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='TEXT')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='media_feed/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube or external video URL")
    hashtags = models.CharField(max_length=200, blank=True, help_text="Space-separated hashtags e.g. #Football #Canon")
    city = models.CharField(max_length=100, default='Yaoundé')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:60]}"

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()

    def hashtag_list(self):
        return [tag.strip() for tag in self.hashtags.split() if tag.startswith('#')]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} on Post #{self.post.id}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} liked Post #{self.post.id}"
