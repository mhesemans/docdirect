from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

STATUS = ((0, "Draft"), (1, "Published"))


class News(models.Model):
    """
    Stores a single news article related to :model:`auth.User`.

    Includes fields for title, slug, author, content, summary, image,
    creation timestamp, and publication status.

    **Fields**:
    - title: Title of the news article.
    - slug: Auto-generated from the title; used for SEO-friendly URLs.
    - author: Foreign key to the User who created the post.
    - content: Full text of the article.
    - Summary: Optional short summary of the article.
    - featured_image: Optional image for the article (via Cloudinary).
    - created_on: Timestamp when created.
    - status: Draft or Published.

    **Meta options**:
    - Orders by most recent first.
    """

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
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
        return f"{self.title} | posted on {self.created_on.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        """
        Automatically generates a unique slug from the title if not set.
        """
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
