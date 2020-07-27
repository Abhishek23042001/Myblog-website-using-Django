from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title= models.CharField(max_length=200)
    content= models.TextField()
    author= models.CharField(max_length=50)
    slug= models.CharField(max_length=100)
    timestamp =models.DateTimeField(blank= True)

    def __str__(self):
        return self.title +' by ' + self.author

class BlogComment(models.Model):
    sno = models.AutoField(primary_key= True)
    comment = models.TextField()
    user= models.ForeignKey(User,on_delete= models.CASCADE) # Blogcomment is associated with User
    post= models.ForeignKey(Post,on_delete= models.CASCADE) # on_delete means if post is deleted than also delete comments coressponding to that post
    parent = models.ForeignKey('self',on_delete= models.CASCADE, null=True) # self means parent is foreignkey of itself
    timestamp= models.DateTimeField(auto_now_add=True, blank= True)

    def __str__(self):
        return self.comment[0:10] + " by " + self.user.username
    