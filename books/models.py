from django.db import models

class Category(models.Model):
    """Category model to classify cookbooks"""
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

class Book(models.Model):
    """Book model to store details about individual cookbooks"""
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=254)
    author = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    review_count = models.DecimalField(max_digits=6, decimal_places=0, null=True, blank=True, default=0)

    def __str__(self):
        return self.title
