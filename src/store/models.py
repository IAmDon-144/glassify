from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Customer
from django.core.validators import MaxValueValidator, MinValueValidator
import random
from django.utils import timezone


def generate_pk():
    number = random.randint(1000, 9999)
    return "{}-{}{}".format("Glassify", timezone.now().strftime('%y%m%d'), number)


class Category(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to='Category', validators=[
                              FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=False)

    

        
    def __str__(self):
        return self.name[0:20]


class Notice(models.Model):
    title = models.CharField(max_length=300)
    code = models.IntegerField(default=0)

            
    def __str__(self):
        return self.title[0:20]

status = (
    ("Available","Available"),
    ("Out of Stock","Out of Stock")
)

class Glasses(models.Model):
    title = models.CharField(max_length=100)
    specification = models.TextField()
    image1 = models.ImageField(upload_to='gallary', validators=[
                               FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=False)
    image2 = models.ImageField(upload_to='gallary', validators=[
                               FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)

    code = models.CharField(default="0000", max_length=255,
                            unique=True,  editable=False)
    liked = models.ManyToManyField(
        Customer, default=None, related_name='likes', blank=True)
        
    cart = models.ManyToManyField(
        Customer, default=None, related_name='cart', blank=True)

    category = models.ManyToManyField(
        Category, default=None, related_name='catagory', blank=False,)
    price = models.IntegerField()
    discount = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ], blank=True)

    productStatus = models.CharField(
        max_length=20, choices=status, default="Available")
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        discountPrice = str(int((100-self.discount)*(self.price/100)))
        self.code = generate_pk() +"-"+ discountPrice
        super(Glasses, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.code)


class Glasses2(models.Model):
    title = models.CharField(max_length=100)
    specification = models.TextField()
    image1 = models.ImageField(upload_to='gallary', validators=[
                               FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=False)
    image2 = models.ImageField(upload_to='gallary', validators=[
                               FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)

    code = models.CharField(default="0000", max_length=255,
                            unique=True,  editable=False)
    liked = models.ManyToManyField(
        Customer, default=None, related_name='likes2', blank=True)
        
    cart = models.ManyToManyField(
        Customer, default=None, related_name='cart2', blank=True)

    category = models.ManyToManyField(
        Category, default=None, related_name='catagory2', blank=False,)
    price = models.IntegerField()
    discount = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ], blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        discountPrice = str(int((100-self.discount)*(self.price/100)))
        self.code = generate_pk() +"-"+ discountPrice
        super(Glasses2, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.code)



class Comment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    post = models.ForeignKey(Glasses, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['-created']
