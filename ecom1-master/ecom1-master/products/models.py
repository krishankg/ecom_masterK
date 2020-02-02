from django.db import models
import random
import os
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.core.signals import request_finished
from django.dispatch import receiver
from django.urls import reverse
def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name,ext=os.path.splitext(base_name)
    return name,ext
def upload_image_path(instance,filename):
    new_file=random.randint(1,72342432)
    name,ext=get_filename_ext(filename)
    final_filename='{}{}'.format(new_file,ext)
    return "products/{}/{}".format(new_file,final_filename)

class ProductManager(models.Manager):
    def get_by_id(self,id):
        return self.get_queryset().filter(id=id)
    def get_by_slug(self,slug):
        return self.get_queryset().filter(slug=slug)

class Product(models.Model):
    name=models.CharField(max_length=50)
    descripation=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=20)
    image=models.ImageField(upload_to=upload_image_path,null=True,blank=True)
    slug=models.SlugField(unique=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    featured=models.BooleanField(default=False)
    active=models.BooleanField(default=True)

    objects=ProductManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail',kwargs={'slug':self.slug})


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        elif Product.objects.filter(slug=self.slug).exists():
            self.slug=slugify(self.name)+'-'+str(random.randint(1,23423))
        return super(Product,self).save(*args,**kwargs)


# @receiver(pre_save)
# def pre_save_receiver(sender, instance, *args, **kwargs):
#    slug = slugify(instance.name)
#    exists = Product.objects.filter(slug=slug).exists()
#    if not exists:
#       return slug
#    else:
#       slug = slug+str(random.int(1,424242))
