from rest_framework import permissions, viewsets
from drf_spectacular.utils import extend_schema
from .serializers import (
    CategorySerializer, ColorSerializer, SizeSerializer, ProductSerializer)
from .models import (Category, Color, Size, Product)
from .permissions import (
    CategoryPermission, ColorPermission, SizePermission, ProductPermission)


@extend_schema(
    description="""Категории""",
    tags=['Category']
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [CategoryPermission,]
    lookup_field = 'slug'


@extend_schema(
    description="""Цвет""",
    tags=['Color']
)
class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all().order_by('name')
    serializer_class = ColorSerializer
    permission_classes = [ColorPermission,]


@extend_schema(
    description="""Размер""",
    tags=['Size']
)
class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all().order_by('name')
    serializer_class = SizeSerializer
    permission_classes = [SizePermission,]


@extend_schema(
    description="""Продукт/товар""",
    tags=['Product']
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [ProductPermission,]
    lookup_field = 'slug'
