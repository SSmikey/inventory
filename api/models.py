from django.db import models
from django.utils import timezone

# ประเภทสินค้า
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # ราคาต่อหน่วย
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# การบันทึกสินค้าเข้า/ออก
class StockTransaction(models.Model):
    TYPE_CHOICES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # สำหรับขาย = quantity * price
    date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # คำนวณ total_price อัตโนมัติถ้าเป็น OUT
        if self.type == 'OUT' and not self.total_price:
            self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.type} - {self.quantity}"
