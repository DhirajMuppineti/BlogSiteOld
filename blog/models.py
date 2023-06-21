from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone



User=get_user_model()



# Create your models here.    
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content= models.TextField()
    written_date = models.DateField(auto_now_add=True)
    lastupdated = models.DateField(default=timezone.now)
    likes = models.IntegerField(default=0)
    
    def likeBlog(self):
        self.likes += 1
        self.save()

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
class LikedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    
    def save(self,*args, **kwargs):
        blog_to_like = Blog.objects.get(pk=self.blog.id)
        blog_to_like.likeBlog()
        super(LikedPost, self).save(*args, **kwargs)