from django.test import TestCase
from django.utils.text import slugify
from .models import Category, Color, Size, Product


class MangaTestCase(TestCase):

    def setUp(self):
        category = Category.objects.create(
            name='category1', slug=slugify('category1'))
        color = Color.objects.create(name='color1', hexa='#00FF04FF')
        size = Size.objects.create(name='size1')
        product1 = Product.objects.create(
            name='product1', category=category, slug=slugify('product1'))
        product1.colors.add(color)
        product1.sizes.add(size)
        product2 = Product.objects.create(
            name='product2', category=category, slug=slugify('product2'))
        product2.colors.add(color)
        product2.sizes.add(size)
        product3 = Product.objects.create(
            name='product3', category=category, slug=slugify('product3'))
        product3.colors.add(color)
        product3.sizes.add(size)

    def test_endpoint_product_execute_query(self):
        with self.assertNumQueries(4):
            """
            count, instance, colors, sizes
            """
            self.client.get('/api/v1/catalog/products/')

        with self.assertNumQueries(3):
            """
            instance, colors, sizes
            """
            self.client.get('/api/v1/catalog/products/product1/')
