from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("new_post_comment/<str:action>", views.new_post_comment, name="new_post_comment"),
    path("user_profile/<int:user_id>", views.user_profile, name="user_profile"),
    path("following", views.following, name="following"),
    path("follow_unfollow/<int:user_id>", views.follow_unfollow, name="follow_unfollow"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
    path("like_comment/<int:comment_id>", views.like_comment, name="like_comment")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)