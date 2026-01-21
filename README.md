# 🛒 Multi-Vendor E-Commerce Backend (Django REST Framework)

A **production-style multi-vendor e-commerce backend** built using **Django REST Framework**, focusing on **real-world backend engineering problems** such as transactional safety, role-based access control, stock consistency, and payment workflows.

This project is designed as a **backend engineer portfolio project**.

---

## 🚀 Features

### 🔐 Authentication & Authorization
- Custom User model
- JWT Authentication (Login / Logout / Refresh)
- Role-based access:
  - **Admin**
  - **Vendor**
  - **Customer**

---

### 🏬 Vendor System
- Vendors linked one-to-one with users
- Vendor verification by admin
- Vendors can manage only their own products

---

### 📦 Product & Category Management
- Category hierarchy (parent-child)
- Vendor-owned products
- Stock & active/inactive control
- Filtering, searching, ordering
- Cursor-based pagination
- Redis caching for product listing

---

### 🛒 Cart System
- Per-user cart
- Quantity validation against available stock
- Automatic removal of inactive products
- Cart summary (total items & total price)

---

### 📑 Order Management
- Orders created from cart
- **Atomic transactions**
- **Row-level locking (`select_for_update`)**
- Stock deduction at order creation
- Prevents overselling
- Cart cleared after successful order

---

### 💳 Payment Flow (Mock Gateway)
- Payment initialization (Stripe sandbox style)
- Payment webhook endpoint
- Order status updated via webhook
- Designed for real payment gateway integration

---

### 🔁 Refund System
- Admin-only refunds
- Order status updated to `CANCELLED`
- Product stock restored automatically

---

### 📊 Admin Analytics
- Total orders
- Total revenue
- Orders per vendor
- Database-level aggregation

---

### ⚡ Performance & Scalability
- Redis caching
- Cursor pagination
- Filtering & searching
- Clean API structure
- Swagger/OpenAPI documentation

---

## 🧰 Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | Django 6, Django REST Framework |
| Database | MySQL |
| Cache | Redis |
| Authentication | JWT (SimpleJWT) |
| API Docs | drf-spectacular (Swagger / OpenAPI) |
| Containerization | Docker, Docker Compose |

---

## 🗂️ Project Structure

