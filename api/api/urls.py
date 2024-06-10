
from rest_framework import routers
from .product.productApi import ProductViewSet
from .user.userApi import UserViewSet

router = routers.DefaultRouter()

router.register('products',ProductViewSet,'products')
router.register('users',UserViewSet,'users')

urlpatterns = router.urls