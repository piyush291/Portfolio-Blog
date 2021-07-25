from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")

class post(models.Model):
 
    objects=models.Manager()           # our default manager-- will return all
    published=PublishedManager()     # our custom manager-- will return only those post with status published


    status_choices=[
        ('draft','Draft'),
        ('published','Published'),
    ]
        


    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=120)   # store and generate valid URLs for your dynamically created web pages.
    author=models.ForeignKey(User, related_name='blog_post',on_delete=models.CASCADE)
    body=models.TextField()
    likes= models.ManyToManyField(User,related_name='likes', blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10, choices = status_choices, default='draft')
    restrict_comment=models.BooleanField(default=False)
    favourite= models.ManyToManyField(User,related_name='favourite', blank=True)

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        # return "blog/%d" %(self.id)
        return reverse("post_details", args=[(self.id)])

    def total_likes(self):
        return self.likes.count()

@receiver(pre_save, sender=post)
def pre_save_slugs(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    dob =  models.DateField(null=True,blank=True)
    photo = models.ImageField(null=True,blank=True)

    def __str__(self):
        return "Profile of user {}".format(self.user.username)


class Images(models.Model):
    post1=models.ForeignKey("post",on_delete=models.CASCADE)
    image=models.ImageField( upload_to="images/", blank=True,null=True)

    def __str__(self):
        return self.post1.title + "image"
    


class comment(models.Model):
    post1=models.ForeignKey(post,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    reply=models.ForeignKey('self',null=True,related_name="replies",on_delete=models.CASCADE)
    content=models.TextField(max_length=160)
    timestamp=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '{}-{}'.format(self.post1.title,str(self.user.username))
