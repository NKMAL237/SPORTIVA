from django.db import models
from django.conf import settings
from organizations.models import SportsCategory


class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('TEXT', 'Text Update'),
        ('IMAGE', 'Photo / Gallery'),
        ('VIDEO', 'Video Highlight'),
        ('SHORT', 'Sportiva Short / Reel'),
        ('ARTICLE', 'Article / Report'),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='TEXT')
    is_short = models.BooleanField(default=False, help_text="Is this a vertical short/reel story")
    sport = models.ForeignKey(
        SportsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='media_feed/', blank=True, null=True)
    video_file = models.FileField(upload_to='media_feed/shorts/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text="YouTube, TikTok, or external video URL")
    hashtags = models.CharField(max_length=200, blank=True, help_text="Space-separated hashtags e.g. #Football #Champions #Training")
    country = models.CharField(max_length=100, default='Global')
    city = models.CharField(max_length=100, default='Global City')
    views_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        type_str = "Short" if self.is_short else self.get_post_type_display()
        return f"[{type_str}] {self.author.username}: {self.content[:50]}"

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()

    def is_liked_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()

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
