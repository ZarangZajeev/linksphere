from django.db import models

from django.contrib.auth.models import User

from datetime import datetime

from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    profile_pic=models.ImageField(upload_to="profilepics",null=True,blank=True)
    dob=models.DateField()
    bio=models.CharField(max_length=200)
    following=models.ManyToManyField("self",related_name="followed_by",symmetrical=False)
    block=models.ManyToManyField("self",related_name="blocked",symmetrical=False)


    def __str__(self):
        return self.user.username
    
class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userpost")
    title=models.CharField(max_length=200)
    post_image=models.ImageField(upload_to="posters",null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User,related_name="post_like")

    def __str__(self):
        return self.title

class Comments(models.Model):
    user=models.ForeignKey(User,related_name="comment",on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Posts,related_name="post_comments",on_delete=models.CASCADE)


    def __str__(self):
        return self.text
    

class Stories(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="userstories")
    title=models.CharField(max_length=200)
    post_image=models.ImageField(upload_to="stories",null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    # exp=created_date + timezone.timedelta(days=1)
    expiry_date=models.DateTimeField()
    

    def __str__(self):
        return self.title
