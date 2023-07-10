"""
URL configuration for dynamic_webapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from blog.views import (
    index,
    login_user,
    register_user,
    logout_user,
    posts,
    post,
    posts_self,
    post_edit,
    post_delete,
    post_create,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("user/login/", login_user, name="login"),
    path("user/register/", register_user, name="register"),
    path("user/logout/", logout_user, name="logout"),
    path("posts/", posts, name="posts"),
    path("post/create/", post_create, name="post_create"),
    path("posts/self/", posts_self, name="posts_self"),
    path("post/<int:post_id>/", post, name="post"),
    path("post/<int:post_id>/edit/", post_edit, name="post_edit"),
    path("post/<int:post_id>/delete/", post_delete, name="post_delete"),
]
