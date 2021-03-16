from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import OrderViewSet, ReportViewSet, ProductViewSet


router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('report', ReportViewSet, basename='report')
router.register('product', ProductViewSet, basename='product')


urlpatterns = router.urls
