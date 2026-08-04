from django.db import models
from apps.core.models import TimeStampedModel
from django.utils.text import slugify

# Create your models here.
class Category(TimeStampedModel):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["title"]