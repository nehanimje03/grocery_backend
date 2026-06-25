# 🛒 Grocery Backend API

A scalable and production-ready RESTful API built for a modern grocery delivery platform.

The Grocery Backend powers product management, inventory, customer accounts, order processing, authentication, and delivery workflows for grocery e-commerce applications.

---

# 🚀 Features

## 👤 Authentication & User Management

* User Registration
* Secure Login and Logout
* JWT Authentication
* Refresh Token Support
* Password Reset Functionality
* User Profile Management
* Role-Based Access Control

## 🛍 Product Management

* Product Listing
* Product Details
* Popular Products
* Latest Arrivals
* Featured Products
* Product Search
* Product Filtering
* Product Variants

## 📂 Category Management

* Category Listing
* Category-Based Product Filtering
* Dynamic Category Management

## 🛒 Shopping Cart

* Add to Cart
* Update Cart Quantity
* Remove Items from Cart
* Cart Summary Calculation

## 📦 Order Management

* Place Orders
* Order History
* Order Status Tracking
* Cancel Orders
* Order Details

## ❤️ Wishlist Management

* Add Products to Wishlist
* Remove Products from Wishlist
* Wishlist Synchronization

## 🔔 Notifications

* Order Confirmation Emails
* Order Status Updates
* Delivery Notifications

## 👨‍💼 Admin Features

* Product Management
* Category Management
* User Management
* Order Monitoring
* Inventory Control
* Sales Management

---

# 🛠 Technology Stack

* Python 3.12+
* Django 5.x
* Django REST Framework
* PostgreSQL
* JWT Authentication
* SMTP Email Service
* CORS Headers
* Pillow
* Git & GitHub
* Postman

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/grocery_backend.git
cd grocery_backend
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

---

## 3️⃣ Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Configure Environment Variables

Create a `.env` file in the project root directory.

```env
DEBUG=True

SECRET_KEY=your_secret_key

ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=grocery_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

ACCESS_TOKEN_LIFETIME=1
REFRESH_TOKEN_LIFETIME=7
```

---

## 6️⃣ Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 7️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

## 8️⃣ Start Development Server

```bash
python manage.py runserver
```

Application will be available at:

```text
http://127.0.0.1:8000/
```

---

# 🔐 Authentication

This project uses JWT Authentication.

Example request header:

```http
Authorization: Bearer <access_token>
```
---

# 🧪 Running Tests

```bash
python manage.py test
```

---

# 🔒 Security Features

* JWT Authentication
* Password Hashing
* Role-Based Authorization
* Protected API Endpoints
* Environment Variable Protection
* CORS Protection
* CSRF Protection

---

# 📈 Future Enhancements

* Online Payment Integration
* Coupon and Discount System
* Real-Time Order Tracking
* Multi-Vendor Support
* Delivery Partner Module
* AI Product Recommendations
* Push Notifications
* Analytics Dashboard

---

# 🚀 Deployment

Recommended production stack:

* Gunicorn
* Nginx
* PostgreSQL
* Docker
* AWS / DigitalOcean / Render

---

# 🤝 Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---
# 👨‍💻 Author

Developed using Django and Django REST Framework for scalable grocery delivery applications.

---

# 🌍 Project Vision

Our vision is to simplify grocery shopping through a fast, secure, and user-friendly digital platform that connects customers with fresh products delivered directly to their doorstep.

The Grocery Backend is designed with scalability, maintainability, and production readiness in mind, making it suitable for startups, enterprises, and modern e-commerce grocery businesses.
