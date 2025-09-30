from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Product, StockTransaction
from .serializers import UserSerializer, ProductSerializer, StockTransactionSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from rest_framework.serializers import ModelSerializer

# -----------------------
# JWT Login
# -----------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

# -----------------------
# Register API
# -----------------------
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # ใครก็สามารถสมัครได้

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # <-- สร้าง user ที่นี่
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {"id": user.id, "username": user.username},
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

# -----------------------
# User View (admin management)
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
