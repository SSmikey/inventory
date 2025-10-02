
# 📦 Inventory Management API

ระบบจัดการสินค้า (Inventory Management) ด้วย Django REST Framework

---

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.2-green?logo=django" alt="django"/>
  <img src="https://img.shields.io/badge/REST%20API-Ready-blue?logo=fastapi" alt="restapi"/>
  <img src="https://img.shields.io/badge/Deploy-Vercel-black?logo=vercel" alt="vercel"/>
</p>

---

## 🗂️ โครงสร้างโปรเจกต์

```
├── manage.py
├── requirements.txt
├── runtime.txt
├── vercel.json
├── README.md
├── api/                # Django app สำหรับ API
│   ├── admin.py
│   ├── apps.py
│   ├── index.py
│   ├── models.py       # โครงสร้างข้อมูลสินค้าและสต็อก
│   ├── serializers.py  # แปลงข้อมูลสำหรับ API
│   ├── tests.py
│   ├── urls.py         # เส้นทาง API
│   ├── views.py        # ฟังก์ชัน API หลัก
│   └── migrations/
│       ├── 0001_initial.py
│       ├── 0002_remove_product_stock_product_description_and_more.py
│       └── __init__.py
└── inventory/          # การตั้งค่าโปรเจกต์ Django
	 ├── settings.py
	 ├── urls.py         # เส้นทางรวม API และ admin
	 ├── asgi.py
	 ├── wsgi.py
	 └── __init__.py
```

---

## ✨ ฟีเจอร์หลัก

- 🔐 **JWT Auth**: สมัคร/เข้าสู่ระบบด้วย JWT Token
- 👤 **User Management**: จัดการผู้ใช้ (admin)
- 📦 **Product CRUD**: เพิ่ม/แก้ไข/ลบ/ดูสินค้า
- 🔄 **Stock Transaction**: บันทึกการเข้า-ออกสินค้า
- 📊 **Dashboard**: สรุปยอดสินค้าและรายงาน 7 วันล่าสุด
- 📈 **Stock Summary**: ดูจำนวนคงเหลือแต่ละสินค้า
- 🌐 **CORS Ready**: เชื่อมต่อกับ Frontend ได้ทันที
- ☁️ **Deploy บน Vercel**

---

## 🛠️ วิธีเริ่มต้นใช้งาน

1. ติดตั้ง dependencies:
	```bash
	pip install -r requirements.txt
	```
2. สร้างไฟล์ .env (หากต้องการปรับแต่งค่าเชื่อมต่อฐานข้อมูล ฯลฯ)
3. รันเซิร์ฟเวอร์:
	```bash
	python manage.py migrate
	python manage.py runserver
	```
4. เข้าสู่ระบบแอดมิน (สร้าง superuser):
	```bash
	python manage.py createsuperuser
	```

---

## 🔗 ตัวอย่าง Endpoint สำคัญ

| Method | URL | Description |
|--------|-----|-------------|
| POST   | /api/register/         | สมัครสมาชิกใหม่ |
| POST   | /api/token/           | รับ JWT Token (login) |
| POST   | /api/token/refresh/   | รีเฟรช Token |
| GET    | /api/products/        | ดูรายการสินค้า (Auth) |
| POST   | /api/products/        | เพิ่มสินค้า (Auth) |
| GET    | /api/stock/           | ดูประวัติ Stock (Auth) |
| POST   | /api/stock/           | บันทึก Stock (IN/OUT) |
| GET    | /api/stock/summary/   | สรุปจำนวนคงเหลือสินค้า |
| GET    | /api/dashboard/       | Dashboard สรุปยอด |

---

## 🧩 เทคโนโลยีที่ใช้

- Django 4.2
- Django REST Framework
- SimpleJWT
- PostgreSQL (แนะนำ)
- Vercel (Deploy)

---

## 📚 ข้อมูลเพิ่มเติม

- ปรับแต่งและขยายระบบได้ง่าย
- เหมาะสำหรับการเรียนรู้และนำไปต่อยอด
- รองรับการเชื่อมต่อกับ Frontend ทุกภาษา

---

<p align="center">
  <b>⚡️ โปรเจกต์นี้เหมาะสำหรับผู้ที่ต้องการระบบ API สำหรับจัดการสินค้าอย่างมืออาชีพ ⚡️</b>
</p>