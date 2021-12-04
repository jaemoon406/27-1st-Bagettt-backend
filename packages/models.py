from django.db      import models


class Package(models.Model):
    name            = models.CharField(max_length=100)
    description     = models.CharField(max_length=2000)
    price           = models.DecimalField(max_digits=9,decimal_places=2)
    thumbnail_image = models.CharField(max_length=2000)
    sales_volume    = models.IntegerField(default=0)
    category        = models.ForeignKey('Category',on_delete=models.CASCADE)
    products        = models.ManyToManyField('Product',related_name='packages')
    tags            = models.ManyToManyField('Tag',related_name='packages')
    
    class Meta:
        db_table = 'packages'

class Product(models.Model):
    name        = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    brand_name  = models.CharField(max_length=200)
    image_url   = models.CharField(max_length=2000)
    kcal        = models.IntegerField()
    nutrition   = models.CharField(max_length=500)

    class Meta:
        db_table = 'products'

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'categories'

class PackageImage(models.Model):
    image_url = models.CharField(max_length=2000)
    packages  = models.ForeignKey('Package',on_delete=models.CASCADE)

    class Meta:
        db_table = 'package_images'

class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'tags'

