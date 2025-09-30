import sys
import os

from django.core.wsgi import get_wsgi_application

# เพิ่ม path ของโปรเจกต์
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ชี้ไปที่ settings ของ inventory
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventory.settings")

app = get_wsgi_application()

# handler ที่ Vercel ใช้เรียก
def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)
