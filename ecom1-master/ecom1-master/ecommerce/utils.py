import random
from django.utils.text import slugify
import string
from random import randint

def random_string_generator(size=10,chars=string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance,new_slug=None):

    if new_slug is not None:
        slug=new_slug
    else:
        slug=slugify(instance.title)
    myclass=instance.__class__
    qs_exists=myclass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug="{slug}-{randomstr}".format(slug=slug,randstr=random_string_generator(size=4))
        return unique_slug_generator(instance,new_slug=new_slug)


def unique_key_generator(instance):
    size=randint(30,45)
    key=random_string_generator(size=size)
    myclass=instance.__class__
    qs_exists=myclass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key




def unique_order_id_generator(instance):
    order_new_id=random_string_generator().upper()
    myclass=instance.__class__
    qs_exists=myclass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)

    return order_new_id
