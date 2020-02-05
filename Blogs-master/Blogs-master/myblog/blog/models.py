from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=120)
    sub_title=models.CharField(max_length=150,blank=True,null=True)
    slug = models.SlugField(max_length=120,blank=True,
                            unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    #photo=models.ImageField(upload_to='post_image/')
    publish = models.DateTimeField(default=timezone.now)
    updated= models.DateTimeField(auto_now=True)
    likes=models.IntegerField(default=0)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    class Meta:
        ordering = ('-publish',)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Post,self).save(*args,**kwargs)

    def __str__(self):
        return self.title



class Comment(models.Model):
    comment_post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment_user=models.ForeignKey(User,on_delete=models.CASCADE)
    comments=models.CharField(max_length=250)
    created_on= models.DateTimeField(default=timezone.now)

    class Meta:
        ordering=('-created_on',)

    def __str__(self):
        return self.comments




class Reply(models.Model):
    comment_posts=models.ForeignKey(Comment,on_delete=models.CASCADE)
    reply_user=models.ForeignKey(User,on_delete=models.CASCADE)
    reply=models.CharField(max_length=250)
    created_on=models.DateTimeField(default=timezone.now)

    class Meta:
        ordering=('-created_on',)

    def __str__(self):
        return self.reply
