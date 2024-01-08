from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    pass

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    about = models.TextField(max_length=225, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    image = models.ImageField(default='profile_pictures/default-user.png', upload_to='profile_pictures')

    def __str__(self):
        return f"{self.user.username}"
    


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"Post {self.id} posted by {self.user.id} on {self.date.strftime('%d/%m/%Y,%H:%M')}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented_by")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=225, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    liked_by = models.ManyToManyField(User, related_name="liked_comment", blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Comment {self.user} on post {self.post.id} by {self.user.username}"
    


class Following(models.Model):
    #Who is doing the following
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    #Who is getting followed
    user_followed = models.ForeignKey(User,on_delete=models.CASCADE, related_name="followers")

    class Meta:
        #User can not follow the same person twice
        unique_together = ['user', 'user_followed']

    def followed_user_posts(self):
        #hasttr(object, attributes)
        if hasattr(self.user_followed, 'posts'):
            return self.user_followed.posts.order_by("-date").all()
        else:
            return None
    
    def __str__(self):
        return f"{self.user} is following {self.user_followed}"
    
