from django.db import models

class navbar(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='navbarImages/')
    slug = models.SlugField(max_length=100, unique=True)


    def __str__(self):
        return self.name
