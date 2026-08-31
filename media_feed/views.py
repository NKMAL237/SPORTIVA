from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from accounts.decorators import tab_required
from .models import Post, Comment, Like


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'title', 'content', 'image', 'video_url', 'hashtags', 'city']
        widgets = {
            'post_type': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'}),
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': 'Post title (optional)'}),
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': "Share a match result, training update, or sports news..."}),
            'image': forms.ClearableFileInput(attrs={'class': 'text-sm text-slate-400'}),
            'video_url': forms.URLInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': 'https://youtube.com/...'}),
            'hashtags': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': '#Football #Canon #Cameroon'}),
            'city': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500'},
                                 choices=[('Yaoundé','Yaoundé'),('Douala','Douala'),('Bafoussam','Bafoussam'),('Garoua','Garoua'),('Bamenda','Bamenda'),('Buea','Buea'),('Maroua','Maroua')]),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'flex-1 px-4 py-3 rounded-xl bg-slate-900 border border-slate-700 text-white text-sm focus:outline-none focus:border-emerald-500', 'placeholder': 'Write a comment...'})
        }


@tab_required('media_feed')
def media_feed_list(request):

    """Main news feed — all published posts, newest first."""
    city_filter = request.GET.get('city', '')
    type_filter = request.GET.get('type', '')
    hashtag_filter = request.GET.get('tag', '')

    queryset = Post.objects.filter(is_published=True).select_related('author')

    if city_filter:
        queryset = queryset.filter(city=city_filter)
    if type_filter:
        queryset = queryset.filter(post_type=type_filter)
    if hashtag_filter:
        queryset = queryset.filter(hashtags__icontains=hashtag_filter)

    # Annotate liked posts for current user
    liked_post_ids = set()
    if request.user.is_authenticated:
        liked_post_ids = set(Like.objects.filter(user=request.user).values_list('post_id', flat=True))

    context = {
        'posts': queryset,
        'liked_post_ids': liked_post_ids,
        'post_form': PostForm(),
        'selected_city': city_filter,
        'selected_type': type_filter,
        'selected_tag': hashtag_filter,
        'post_types': Post.POST_TYPE_CHOICES,
    }
    return render(request, 'media_feed/list.html', context)


@login_required
def post_create(request):
    """Create a new post in the sports feed."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been published!")
            return redirect('media_feed_list')
    else:
        form = PostForm()
    return render(request, 'media_feed/create.html', {'form': form})


def post_detail(request, pk):
    """Detailed post view with comments."""
    post = get_object_or_404(Post.objects.select_related('author'), pk=pk, is_published=True)
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
    return redirect(request.META.get('HTTP_REFERER', 'media_feed_list'))
