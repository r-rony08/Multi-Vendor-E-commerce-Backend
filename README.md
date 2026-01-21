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
```text
e-commerce/
├── users/
├── vendors/
├── products/
├── carts/
├── orders/
├── payments/
├── analytics/
├── docker-compose.yml
├── Dockerfile
└── README.md
```
# API Documentation
Swagger UI: http://127.0.0.1:8000/api/docs/

## 👤 Authentication & Users (`/users/`)

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/users/register/` | Register a new user (customer/vendor) |
| POST | `/users/login/` | Obtain JWT access & refresh tokens |
| POST | `/users/logout/` | Logout user (blacklist refresh token) |
| POST | `/users/token/refresh/` | Refresh JWT access token |
| GET | `/users/profile/` | Get authenticated user profile |

---

## 🏬 Vendors (`/vendors/`)

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/vendors/create/` | Create vendor profile (vendor user only) |
| GET | `/vendors/me/` | Get current vendor details |
| PATCH | `/vendors/me/` | Update vendor profile |
| GET | `/vendors/` | List all verified vendors |
| PATCH | `/vendors/{id}/verify/` | Verify vendor (admin only) |

---

## 📦 Categories (`/products/categories/`)

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/products/categories/` | Create category (admin only) |
| GET | `/products/categories/` | List all categories |
| GET | `/products/categories/{id}/` | Retrieve single category |
| PATCH | `/products/categories/{id}/` | Update category |
| DELETE | `/products/categories/{id}/` | Delete category |

---

## 🛍️ Products (`/products/`)

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/products/` | Create product (vendor only) |
| GET | `/products/` | List products (search, filter, pagination, cached) |
| GET | `/products/{id}/` | Retrieve product details |
| PATCH | `/products/{id}/` | Update product (owner vendor only) |
| DELETE | `/products/{id}/` | Delete product (owner vendor only) |
| GET | `/products/vendor/` | List products of logged-in vendor |

---

## 🛒 Cart (`/carts/`)

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/carts/items/` | Add product to cart |
| GET | `/carts/items/` | List cart items |
| PATCH | `/carts/items/{id}/` | Update cart item quantity |
| DELETE | `/carts/items/{id}/` | Remove item from cart |
| GET | `/carts/summary/` | Get cart total items & total price |

---

## 📑 Orders (`/orders/`)

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/orders/create/` | Create order from cart (atomic & stock-safe) |
| GET | `/orders/` | List user orders |
| GET | `/orders/{id}/` | Retrieve order details |
| POST | `/orders/{id}/refund/` | Refund order (admin only) |

---

## 💳 Payments (`/payments/`)

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/payments/initiate/` | Initiate payment for an order |
| POST | `/payments/webhook/` | Payment gateway webhook |
| GET | `/payments/{id}/` | Retrieve payment details |

---

## 📊 Analytics (`/analytics/`) — Admin Only

| Method | Endpoint | Description |
|------|---------|-------------|
| GET | `/analytics/summary/` | Platform-wide stats (orders, revenue) |
| GET | `/analytics/vendors/` | Revenue & orders per vendor |

---

## 📄 API Documentation

| Tool | URL |
|----|----|
| Swagger UI | `/api/docs/` |
| OpenAPI Schema | `/api/schema/` |

---

## 🔐 Permissions Summary

- **Customer**: Cart, orders, payments
- **Vendor**: Products, vendor profile
- **Admin**: Verify vendors, refunds, analytics
- **Public**: Product & category listing

---

## How to Run Locally
```bash
git clone https://github.com/your-username/jobtrackr.git](https://github.com/r-rony08/Multi-Vendor-E-commerce-Backend.git
```
### Create a .env file in the root directory
```ini
DEBUG=True
SECRET_KEY=your django key password
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Settings
DB_NAME=e_commerce
DB_USER=root
DB_PASSWORD=your_local_password
DB_HOST=localhost
DB_PORT=3306
```
```bash
# Create database
CREATE DATABASE e_commerce;

# Activate Virtual Environment
python -m venv env

# On Windows:
env\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run Migrations and Start Server
python manage.py migrate
python manage.py runserver
```
