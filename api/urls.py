from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, TransactionViewSet, dashboard_summary
from django.urls import path

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = router.urls + [
    path("dashboard/", dashboard_summary, name="dashboard"),
]
