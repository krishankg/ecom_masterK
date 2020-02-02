from django.db import models
from django.utils.text import slugify
import random
from products.models import Product
class Tag(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(unique=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    products=models.ManyToManyField(Product,blank=True)

    def __str__(self):
        return self.title


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        elif Tag.objects.filter(slug=self.slug).exists():
            self.slug=slugify(self.title)+'-'+str(random.randint(1,23423))
        super(Tag,self).save(*args,**kwargs)
