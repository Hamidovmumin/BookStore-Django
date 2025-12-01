from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name='Category'
        verbose_name_plural='Categories' # admin paneldə bölmənin adını dəyişdirir.

    def __str__(self):
        return self.category_name