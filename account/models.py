from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import default, slugify
from django.core.urlresolvers import reverse 

from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager): #This is the custom manager
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')   


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    
    class Meta:
        ordering = ('-publish',)
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('account:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])
     
    def save(self):
        super(Post, self).save()
        self.slug = '%s' %(slugify(self.title))
        super(Post, self).save()
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
        
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%y/%m/%d',
                              blank=True)
    def __str__(self):
        return 'Profile for user {}'.fromat(self.user.username)