from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProductViewSet, StockTransactionViewSet,
    DashboardView, CustomTokenObtainPairView, RegisterView
)
from rest_framework_simplejwt.views import TokenRefreshView
from .views import StockSummaryView

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("products", ProductViewSet)
router.register("stock", StockTransactionViewSet)

urlpatterns = [
    path('stock/summary/', StockSummaryView.as_view(), name='stock-summary'),
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("", include(router.urls)),
]
