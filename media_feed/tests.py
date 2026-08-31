from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from media_feed.models import Post, Like, Comment


class MediaFeedFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='creatoruser',
            email='creator@example.com',
            password='strongpass123',
            role=User.Role.ATHLETE,
        )
        self.post = Post.objects.create(
            author=self.user,
            post_type='TEXT',
            title='Training update',
            content='Morning training was excellent and the team is ready for the next match.',
            city='Yaoundé',
        )

    def test_media_feed_list_page_loads(self):
        response = self.client.get(reverse('media_feed_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sports News & Highlights')

    def test_post_detail_page_loads(self):
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_post_create_requires_login(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_post_create_post(self):
        self.client.login(username='creatoruser', password='strongpass123')
        response = self.client.post(reverse('post_create'), {
            'post_type': 'TEXT',
            'title': 'Match Result',
            'content': 'We won 2-1 against Canon Yaoundé!',
            'city': 'Yaoundé',
            'hashtags': '#Victory #Cameroon',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='Match Result').exists())

    def test_post_like_toggle(self):
        self.client.login(username='creatoruser', password='strongpass123')
        response = self.client.post(reverse('post_like', args=[self.post.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(post=self.post, user=self.user).exists())

    def test_post_comment_add(self):
        self.client.login(username='creatoruser', password='strongpass123')
        response = self.client.post(reverse('post_detail', args=[self.post.pk]), {
            'content': 'Great post!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post, content='Great post!').exists())
