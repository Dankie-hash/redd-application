from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Section(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    colour = models.CharField(max_length=20, unique=True)
    created_by = models.ForeignKey(User, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        return reverse('app:section', args=[self.pk])

    class Meta:
        db_table = 'section'

class Post(models.Model):

    title = models.CharField(max_length=300)
    text = models.TextField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)


    def __str__(self):
        return self.title[:12]

    def get_absolute_url(self):
        return reverse('app:post', args=[self.pk])

    def mini_post(self):
        return self.text[:200]+'...'

    class Meta:
        db_table = 'post'


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_on = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)


    def __str__(self):
        return self.user.username + self.text[:12]

    def get_absolute_url(self):
        return reverse('app:', args=[self.pk])

    class Meta:
        db_table = 'comment'

