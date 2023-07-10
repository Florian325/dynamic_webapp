from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from blog.models import Article, Comment

# Create your views here.


def index(request):
    return render(request, "index.html")


def login_user(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print("User logged in")
            return redirect("index")
        return render(request, "user/login.html", {"error": "Invalid credentials"})
    return render(request, "user/login.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password != password2:
            return render(
                request, "user/register.html", {"error": "Passwords do not match"}
            )
        if username is None or password is None:
            return render(
                request, "user/register.html", {"error": "Username or password missing"}
            )
        if len(username) < 4 or len(password) < 4:
            return render(
                request,
                "user/register.html",
                {"error": "Username or password too short"},
            )
        if len(username) > 20 or len(password) > 20:
            return render(
                request,
                "user/register.html",
                {"error": "Username or password too long"},
            )
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "user/register.html",
                {"error": "Username already exists"},
            )
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        user.save()

        return redirect("index")

    return render(request, "user/register.html")


def logout_user(request):
    logout(request)
    return redirect("index")


def posts(request):
    if not request.user.is_authenticated:
        return redirect("index")
    posts = Article.objects.all()
    return render(request, "posts.html", {"posts": posts})


def posts_self(request):
    if not request.user.is_authenticated:
        return redirect("index")
    # posts = Article.objects.filter(author=request.user)
    posts = request.user.posts.all()
    return render(request, "posts.html", {"posts": posts})


def post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("index")

    try:
        post = Article.objects.get(id=post_id)
    except Article.DoesNotExist:
        return redirect("posts")

    return render(request, "post.html", {"post": post})


def post_edit(request, post_id):
    if not request.user.is_authenticated:
        return redirect("index")

    try:
        post = Article.objects.get(id=post_id)
    except Article.DoesNotExist:
        return redirect("posts")

    if post.author != request.user:
        return redirect("posts")

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title is None or content is None:
            return render(
                request, "post_edit.html", {"error": "Title or content missing"}
            )
        if len(title) > 200:
            return render(request, "post_edit.html", {"error": "Title too long"})
        post.title = title
        post.content = content
        post.save()
        return redirect("post", post_id=post.id)

    return render(request, "post_edit.html", {"post": post})


def post_delete(request, post_id):
    if not request.user.is_authenticated:
        return redirect("index")

    try:
        post = Article.objects.get(id=post_id)
    except Article.DoesNotExist:
        return redirect("posts")

    if post.author != request.user:
        return redirect("posts")

    post.delete()
    return redirect("posts")


def post_create(request):
    if not request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title is None or content is None:
            return render(
                request, "post_edit.html", {"error": "Title or content missing"}
            )
        if len(title) > 200:
            return render(request, "post_edit.html", {"error": "Title too long"})
        post = Article(title=title, content=content, author=request.user)
        post.save()

        return redirect("post", post_id=post.id)

    return render(request, "post_create.html")
