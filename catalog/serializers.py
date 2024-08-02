from rest_framework import serializers
from .models import (Category, Size, Color, Product)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'url', 'name']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ColorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'url', 'name', 'hexa']


class SizeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'url', 'name']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    colors = ColorSerializer(many=True)
    sizes = SizeSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'category', 'colors', 'sizes']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
