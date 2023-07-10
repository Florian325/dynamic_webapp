# dynamic_webapp with Django
Only a small demo project for school to show the basics of Django.

# Erklärungen
```python
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from blog.models import Article, Comment


```
Dieser Codeabschnitt importiert die notwendigen Module und Modelle, die für die Implementierung der Funktionen in diesem Modul benötigt werden.

```python
def index(request):
    return render(request, "index.html")
```
Diese Funktion gibt die index.html-Seite zurück, wenn sie aufgerufen wird.

```python
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
```
Diese Funktion authentifiziert einen Benutzer, wenn er sich anmeldet. Wenn der Benutzer bereits angemeldet ist, wird er zur Startseite weitergeleitet. Wenn der Benutzername und das Passwort korrekt sind, wird der Benutzer angemeldet und zur Startseite weitergeleitet. Andernfalls wird eine Fehlermeldung angezeigt.

```python
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
```
Diese Funktion registriert einen neuen Benutzer. Wenn das Passwort nicht mit der Bestätigung übereinstimmt, wird eine Fehlermeldung angezeigt. Wenn der Benutzername oder das Passwort fehlt oder zu kurz oder zu lang ist, wird eine Fehlermeldung angezeigt. Wenn der Benutzername bereits existiert, wird eine Fehlermeldung angezeigt. Andernfalls wird der Benutzer registriert, angemeldet und zur Startseite weitergeleitet.

```python
def logout_user(request):
    logout(request)
    return redirect("index")
```
Diese Funktion meldet den Benutzer ab und leitet ihn zur Startseite weiter.

```python
def posts(request):
    if not request.user.is_authenticated:
        return redirect("index")
    posts = Article.objects.all()
    return render(request, "posts.html", {"posts": posts})
```
Diese Funktion gibt alle Artikel auf der posts.html-Seite zurück, wenn der Benutzer angemeldet ist.

```python
def posts_self(request):
    if not request.user.is_authenticated:
        return redirect("index")
    # posts = Article.objects.filter(author=request.user)
    posts = request.user.posts.all()
    return render(request, "posts.html", {"posts": posts})
```
Diese Funktion gibt alle Artikel des angemeldeten Benutzers auf der posts.html-Seite zurück.

```python
def post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("index")

    try:
        post = Article.objects.get(id=post_id)
    except Article.DoesNotExist:
        return redirect("posts")

    return render(request, "post.html", {"post": post})
```
Diese Funktion gibt einen bestimmten Artikel auf der post.html-Seite zurück, wenn der Benutzer angemeldet ist.

```python
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
```
Diese Funktion bearbeitet einen bestimmten Artikel, wenn der Benutzer angemeldet ist und der Autor des Artikels ist. Wenn der Titel oder der Inhalt fehlt oder der Titel zu lang ist, wird eine Fehlermeldung angezeigt. Andernfalls wird der Artikel bearbeitet und zur post.html-Seite weitergeleitet.

```python
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
```
Diese Funktion löscht einen bestimmten Artikel, wenn der Benutzer angemeldet ist und der Autor des Artikels ist.

```python
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
```
Diese Funktion erstellt einen neuen Artikel, wenn der Benutzer angemeldet ist. Wenn der Titel oder der Inhalt fehlt oder der Titel zu lang ist, wird eine Fehlermeldung angezeigt. Andernfalls wird der Artikel erstellt und zur post.html-Seite weitergeleitet.
