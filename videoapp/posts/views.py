from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Like, SavedPost
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

@login_required
def create_post(request, post_type):
    # form fields filtreleme
    form = PostForm(request.POST or None, request.FILES or None)
    
    # sadece ilgili alanları kullan
    if post_type == "text":
        form.fields.pop("image")
        form.fields.pop("video")
    elif post_type == "image":
        form.fields.pop("video")
    elif post_type == "video":
        form.fields.pop("image")
    else:
        messages.error(request, "Geçersiz gönderi türü.")
        return redirect('posts:explore')

    if request.method == "POST" and form.is_valid():
        p = form.save(commit=False)
        p.user = request.user
        p.save()
        messages.success(request, f"{post_type.capitalize()} gönderiniz paylaşıldı!")
        return redirect('posts:user_posts', username=request.user.username)

    return render(request, "posts/create_post.html", {"form": form, "post_type": post_type})

def explore(request):
    posts = Post.objects.select_related('user').prefetch_related('likes','comments')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)

    # Kullanıcı için like ve save durumlarını ekleyelim
    for post in posts_page:
        if request.user.is_authenticated:
            post.is_liked = post.likes.filter(user=request.user).exists()
            post.is_saved = post.saved_by.filter(user=request.user).exists()
        else:
            post.is_liked = False
            post.is_saved = False

    return render(request, "posts/explore.html", {"posts": posts_page})

def user_posts(request, username):
    from users.models import UserModel
    user = get_object_or_404(UserModel, username=username)
    posts = user.posts.all().select_related('user').prefetch_related('likes','comments')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    return render(request, "posts/user_posts.html", {
        "posts": paginator.get_page(page),
        "profile_user": user
    })

def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('user').prefetch_related('comments__user','likes','saved_by'), pk=pk)
    
    comment_form = CommentForm()
    
    # Kullanıcının like ve kaydetme durumlarını kontrol et
    user_liked = False
    user_saved = False
    if request.user.is_authenticated:
        user_liked = post.likes.filter(user=request.user).exists()
        user_saved = post.saved_by.filter(user=request.user).exists()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            c = comment_form.save(commit=False)
            c.post = post
            c.user = request.user
            c.save()
            messages.success(request, "Yorum eklendi.")
            return redirect('posts:post_detail', pk=post.pk)

    return render(request, "posts/post_detail.html", {
        "post": post,
        "comment_form": comment_form,
        "user_liked": user_liked,
        "user_saved": user_saved,
    })


@login_required
@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if created:
        post.like_count += 1
        post.save(update_fields=['like_count'])
    else:
        like.delete()
        if post.like_count > 0:
            post.like_count -= 1
            post.save(update_fields=['like_count'])

    return redirect(request.META.get('HTTP_REFERER', 'posts:explore'))


@login_required
@require_POST
def toggle_save(request, pk):
    post = get_object_or_404(Post, pk=pk)
    saved, created = SavedPost.objects.get_or_create(post=post, user=request.user)
    if not created:
        saved.delete()
    return redirect(request.META.get('HTTP_REFERER', 'posts:explore'))

