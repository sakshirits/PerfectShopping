from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250,unique=True)
    slug = models.SlugField(max_length=250,unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images')

    class Meta:
      ordering = ('name',)
      verbose_name = 'category'


    def __str__(self):
       return self.name

    def get_url(self):
        return reverse('shop:products_by_category',args=[self.slug])

class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='products')
    stock  = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
       ordering = ('name',)
       verbose_name = 'product'

    def __str__(self):
       return self.name

    def get_url(self):
        return reverse('shop:prod_details',args=[self.category.slug,self.slug])


