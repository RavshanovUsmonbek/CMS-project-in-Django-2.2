from django.db import models
from django import forms
from django.contrib.auth.models import User


# Create your models here.
class Catagory(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_title = models.CharField(max_length=256)

    def __str__(self):
        return self.cat_title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    user_image = models.ImageField(upload_to = 'users_pics', blank = True)
    user_isAdmin = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_cat_id = models.ForeignKey(Catagory, on_delete = models.SET_NULL, null =True)
    post_title = models.CharField(max_length =256)
    post_author = models.ForeignKey(User, on_delete=models.SET_NULL,  null =True)
    post_date = models.DateField(auto_now_add=True)
    post_image = models.ImageField(upload_to = 'posts_pics', blank = True)
    post_content = models.TextField()
    post_tags = models.CharField(max_length=256, blank = True)
    post_comment_count = models.IntegerField(blank=True, default=0)
    post_status = models.CharField(max_length=256)

    def __str__(self):
        return self.post_title

class Comment(models.Model):
    com_id= models.AutoField(primary_key=True)
    com_post_id = models.ForeignKey(Post, on_delete = models.CASCADE)
    com_author = models.ForeignKey(User,on_delete = models.SET_NULL, null = True)
    com_content = models.TextField()
    com_status = models.CharField(max_length=256)
    com_date = models.DateField(auto_now_add=True)
