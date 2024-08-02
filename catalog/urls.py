from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories',
                views.CategoryViewSet, basename='category')
router.register(r'colors', views.ColorViewSet, basename='color')
router.register(r'sizes', views.SizeViewSet, basename='size')
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls))
]
