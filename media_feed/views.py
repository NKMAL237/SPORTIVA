from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.decorators import tab_required
from organizations.models import SportsCategory
from .models import Post, Comment, Like


FEED_TABS = [
    ('for_you', _('For You'), 'fa-wand-magic-sparkles'),
    ('following', _('Following'), 'fa-user-group'),
    ('shorts', _('Shorts & Reels'), 'fa-clapperboard'),
    ('trending', _('Trending'), 'fa-fire'),
]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'is_short', 'sport', 'title', 'content', 'image', 'video_file', 'video_url', 'hashtags', 'country', 'city']
        widgets = {
            'post_type': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'is_short': forms.CheckboxInput(attrs={'class': 'rounded border-slate-600 bg-slate-900 text-cyan-500'}),
            'sport': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'placeholder': 'Post title / headline (optional)'}),
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'placeholder': "What's your latest sports achievement, training moment, or highlight?..."}),
            'video_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'placeholder': 'https://youtube.com/shorts/... or https://tiktok.com/...'}),
            'hashtags': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'placeholder': '#Football #Training #Workout #Exploit'}),
            'country': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['title', 'sport', 'is_short', 'image', 'video_file', 'video_url', 'hashtags', 'country', 'city']:
            if field_name in self.fields:
                self.fields[field_name].required = False


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'flex-1 px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-cyan-500', 'placeholder': 'Write a comment...'})
        }


@tab_required('media_feed')
def media_feed_list(request):
    """
    Main News & Feed (Instagram-style feed):
    Supports 'For You' (personalized according to user's favorite sports),
    'Following' (posts from subscribed athletes/clubs/sponsors),
    'Trending' (highest liked posts), and 'Shorts' (vertical video reels).
    """
    tab = request.GET.get('tab', 'for_you')  # for_you, following, shorts, trending
    sport_filter = request.GET.get('sport', '')
    hashtag_filter = request.GET.get('tag', '')

    queryset = Post.objects.filter(is_published=True).select_related('author', 'sport').prefetch_related('likes', 'comments')

    if sport_filter:
        queryset = queryset.filter(sport__id=sport_filter)
    if hashtag_filter:
        queryset = queryset.filter(hashtags__icontains=hashtag_filter)

    # Top horizontal stories / shorts list
    top_shorts = Post.objects.filter(is_published=True, is_short=True).select_related('author', 'sport')[:10]

    posts = list(queryset)

    liked_post_ids = set()
    followed_ids = set()
    if request.user.is_authenticated:
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))
        followed_ids = set(request.user.following.values_list('followed_user_id', flat=True))

    # Personalization Logic
    if tab == 'for_you' and request.user.is_authenticated:
        fav_sports = [s.lower() for s in (request.user.favorite_sports or [])]
        if fav_sports:
            def sport_priority(post):
                if post.sport and post.sport.name.lower() in fav_sports:
                    return 0
                return 1
            posts.sort(key=sport_priority)
    elif tab == 'following':
        posts = [p for p in posts if p.author_id in followed_ids]
    elif tab == 'shorts':
        posts = [p for p in posts if p.is_short]
    elif tab == 'trending':
        posts.sort(key=lambda p: p.like_count(), reverse=True)

    sports = SportsCategory.objects.all()

    context = {
        'posts': posts,
        'top_shorts': top_shorts,
        'liked_post_ids': liked_post_ids,
        'followed_ids': followed_ids,
        'post_form': PostForm(),
        'active_tab': tab,
        'feed_tabs': FEED_TABS,
        'sports': sports,
        'selected_sport': sport_filter,
        'selected_tag': hashtag_filter,
    }
    return render(request, 'media_feed/list.html', context)


@login_required
def post_create(request):
    """Create a new post or video short in the feed."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if request.POST.get('is_short') == 'on' or post.post_type == 'SHORT':
                post.is_short = True
                post.post_type = 'SHORT'
            post.save()
            messages.success(request, "Your moment has been shared with the SPORTIVA community! 🚀")
            return redirect('media_feed_list')
    else:
        form = PostForm()
    return render(request, 'media_feed/create.html', {'form': form})


def post_detail(request, pk):
    """Detailed post view with comments."""
    post = get_object_or_404(Post.objects.select_related('author', 'sport'), pk=pk, is_published=True)
    comments = post.comments.select_related('author').all()
    comment_form = CommentForm()
    is_liked = request.user.is_authenticated and Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added!")
            return redirect('post_detail', pk=pk)

    return render(request, 'media_feed/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
    })


@login_required
def post_like(request, pk):
    """Toggle like on a post."""
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/media-feed/'
    return redirect(next_url)
