from django.db import models
from apps.core.models import TimeStampedModel
from apps.categories.models import Category
from django.utils.text import slugify

# Create your models here.
class MenuItem(TimeStampedModel):
    slug = models.SlugField(unique=True, )
    item_image = models.ImageField(blank=True, upload_to="menu/item_images", )
    title = models.CharField(max_length=50, unique=True, )
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField()
    preparation_time = models.DurationField()
    calories = models.FloatField()

    def __str__(self):
        return f"{self.title} - {self.price}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while MenuItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["title"]