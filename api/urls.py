from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProductViewSet, StockTransactionViewSet,
    DashboardView, CustomTokenObtainPairView, RegisterView
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register("users", UserViewSet)          # admin-only
router.register("products", ProductViewSet)    # CRUD products
router.register("stock", StockTransactionViewSet)  # CRUD stock transactions

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),  # anyone can register
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),  # login
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),       # refresh token
    path("dashboard/", DashboardView.as_view(), name="dashboard"),  # dashboard stats
    path("", include(router.urls)),  # router urls for users, products, stock
]
