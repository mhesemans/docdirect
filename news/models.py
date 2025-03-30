from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


# Create your models here.
"""
stores a single blog post entry  related to :model: `auth.User`.

"""


class News(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="news_items"
    )
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    Summary = models.TextField(blank=True)
    featured_image = CloudinaryField('image', default='placeholder')

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | posted on {self.created_on}"
