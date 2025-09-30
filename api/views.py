from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Product, StockTransaction
from .serializers import UserSerializer, ProductSerializer, StockTransactionSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView

# -----------------------
# JWT Login
# -----------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

# -----------------------
# Register API
# -----------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # <<< สร้าง user ตรงนี้

        return Response({
            "message": "Register success",
            "user": {
                "id": user.id,
                "username": user.username
            }
        }, status=201)

# -----------------------
# User View (admin only)
# -----------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

# -----------------------
# Product CRUD
# -----------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

# -----------------------
# Stock Transaction
# -----------------------
class StockTransactionViewSet(viewsets.ModelViewSet):
    queryset = StockTransaction.objects.all()
    serializer_class = StockTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

# -----------------------
# Dashboard data
# -----------------------
class DashboardView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        total_products = Product.objects.count()
        total_stock_in = StockTransaction.objects.filter(type='IN').aggregate(total=Sum('quantity'))['total'] or 0
        total_stock_out = StockTransaction.objects.filter(type='OUT').aggregate(total=Sum('quantity'))['total'] or 0
        total_revenue = StockTransaction.objects.filter(type='OUT').aggregate(total=Sum('total_price'))['total'] or 0

        # Last 7 days transaction chart
        today = timezone.now().date()
        chart_data = []
        for i in range(7):
            day = today - timedelta(days=i)
            in_count = StockTransaction.objects.filter(type='IN', date__date=day).aggregate(total=Sum('quantity'))['total'] or 0
            out_count = StockTransaction.objects.filter(type='OUT', date__date=day).aggregate(total=Sum('quantity'))['total'] or 0
            chart_data.append({
                "date": str(day),
                "in": in_count,
                "out": out_count
            })

        return Response({
            "total_products": total_products,
            "total_stock_in": total_stock_in,
            "total_stock_out": total_stock_out,
            "total_revenue": total_revenue,
            "chart_data": chart_data[::-1]  # oldest first
        })

class StockSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # ดึงสินค้าทั้งหมด
        products = Product.objects.all()
        summary = []

        for product in products:
            # คำนวณจำนวนสินค้าคงเหลือ: sum of IN - sum of OUT
            stock_in = StockTransaction.objects.filter(product=product, type='IN').aggregate(total=Sum('quantity'))['total'] or 0
            stock_out = StockTransaction.objects.filter(product=product, type='OUT').aggregate(total=Sum('quantity'))['total'] or 0
            current_stock = stock_in - stock_out

            summary.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': current_stock
            })

        return Response(summary)