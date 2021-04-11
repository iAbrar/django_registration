from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    date_posted = models.DateTimeField()
    author = models.CharField(max_length=70)
    image_url = models.URLField()
    slug = models.SlugField()
    likes = models.ManyToManyField("users.User", related_name= 'blog_posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={
            'slug': self.slug
        })

