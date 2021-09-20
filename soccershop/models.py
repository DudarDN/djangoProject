from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('soccershop:product_list_by_category',
                       args=[self.slug])


class SizeType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Size(models.Model):
    sizetype = models.ForeignKey(SizeType, related_name='sizes',
                                 on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    class Meta:
        ordering = ('sizetype',)

    def __str__(self):
        return self.value


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    sizetype = models.ForeignKey(SizeType,
                                 related_name='products',
                                 on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('soccershop:product_detail',
                       args=[self.id, self.slug])


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Review by {} on {}'.format(self.name, self.product)


