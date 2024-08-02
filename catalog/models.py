from django.db import models
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, help_text=_(
        'Enter the name of the product category'))
    slug = models.SlugField(max_length=128, db_index=True, unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            help_text=_('Enter the name of the size'))

    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            help_text=_('Enter the name of the color'))
    hexa = ColorField(format="hexa")

    class Meta:
        verbose_name = _('Color')
        verbose_name_plural = _('Colors')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True,
                            help_text=_('Enter the name of the product'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    colors = models.ManyToManyField(Color, blank=True, related_name='products', help_text=_(
        'Enter the colors of the product'))
    sizes = models.ManyToManyField(Size, blank=True, related_name='products', help_text=_(
        'Enter the sizes of the product'))
    slug = models.SlugField(max_length=128, db_index=True, unique=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name
