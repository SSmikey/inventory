from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, F
from django.utils import timezone
from django.db.models.functions import TruncDate
import uuid

from .models import Product, Transaction
from .serializers import ProductSerializer, TransactionSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by("-created_at")
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.setdefault("id", str(uuid.uuid4()))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        tx = serializer.save()
        prod = tx.product
        if tx.type == "out":
            prod.stock = F('stock') - tx.quantity
        else:
            prod.stock = F('stock') + tx.quantity
        prod.save()
        prod.refresh_from_db()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def dashboard_summary(request):
    total_products = Product.objects.count()
    total_stock = Product.objects.aggregate(total_stock=Sum("stock"))["total_stock"] or 0
    sold_qty = Transaction.objects.filter(type="out").aggregate(sold=Sum("quantity"))["sold"] or 0
    revenue = Transaction.objects.filter(type="out").aggregate(revenue=Sum("total_price"))["revenue"] or 0

    qs = (Transaction.objects
          .filter(created_at__gte=timezone.now() - timezone.timedelta(days=14), type="out")
          .annotate(day=TruncDate("created_at"))
          .values("day")
          .annotate(total_qty=Sum("quantity"), total_revenue=Sum("total_price"))
          .order_by("day"))
    daily = [{"day": r["day"], "qty": r["total_qty"], "revenue": float(r["total_revenue"] or 0)} for r in qs]

    return Response({
        "total_products": total_products,
        "total_stock": total_stock,
        "sold_qty": sold_qty,
        "revenue": float(revenue),
        "daily": daily
    })
