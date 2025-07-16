# Courier Management System - Backend API

This is the backend REST API for a Courier Management System built with Django REST Framework and JWT authentication.

## 🌐 Live API

**Base URL:** [https://courier-management-system-backendapi.onrender.com](https://courier-management-system-backendapi.onrender.com/api/v1/)  
**Postman Documentation:** [https://documenter.getpostman.com/view/46111276/2sB34eGgp7](https://documenter.getpostman.com/view/46111276/2sB34eGgp7)

---

## 📦 Features

- User Registration & JWT Login
- Admin/User/Delivery Man Roles
- Order Creation & Assignment
- Stripe Payment Integration
- Secure Role-Based Access
- Full CRUD for Orders (Admin/Delivery only)
- API Documentation & Postman Support

---

## 🚀 Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/your-username/courier-management-system-backend.git
cd courier-management-system-backend
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # on Windows use: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a .env or set in settings.py: 
```bash
STRIPE_SECRET_KEY=your_stripe_secret_key
```

5. **Run migrations and start server**
```bash
python manage.py migrate
python manage.py runserver
```

## 🧪 API Endpoints

| Method | Endpoint                   | Description                       |
| ------ | -------------------------- | --------------------------------- |
| POST   | `/api/v1/register/`        | Register user                     |
| POST   | `/api/v1/login/`           | Login (JWT)                       |
| POST   | `/api/v1/token/refresh/`   | Refresh JWT token                 |
| GET    | `/api/v1/profile/`         | View user profile                 |
| GET    | `/api/v1/orders/`          | List orders                       |
| POST   | `/api/v1/orders/`          | Create order                      |
| PATCH  | `/api/v1/orders/<id>/`     | Update order (Admin/Delivery Man) |
| DELETE | `/api/v1/orders/<id>/`     | Delete order (Admin)              |
| GET    | `/api/v1/orders/assigned/` | Delivery Man’s assigned orders    |
| POST   | `/api/v1/orders/<id>/pay/` | Initiate Stripe payment           |
| GET    | `/api/v1/users/`           | List users (Admin only)           |


# 📦 API Documentation

**Base URL:**\
**Production**: `https://courier-management-system-backendapi.onrender.com/api/v1/`\
**Local**: `http://127.0.0.1:8000/api/v1/`

---

## 📁 Auth Endpoints

### 🔐 Register User

**POST** `/auth/register/`\
Registers a new user (Admin, Delivery Man, or User).

#### Request Body:

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "TestPass123",
  "password2": "TestPass123",
  "role": "USER"  // or "ADMIN", "DELIVERY_MAN"
}
```

#### Response:

```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "role": "user"
}
```

---

### 🔑 Login

**POST** `/auth/login/`

#### Request Body:

```json
{
  "username": "john",
  "password": "TestPass123"
}
```

#### Response:

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Login successful",
  "Data": {
    "access": "jwt-access-token",
    "refresh": "jwt-refresh-token",
    "user": {
      "id": 1,
      "username": "john",
      "email": "john@example.com",
      "role": "user"
    }
  }
}
```

---

### 🔄 Refresh Token

**POST** `/token/refresh/`

#### Request Body:

```json
{
  "refresh": "jwt-refresh-token"
}
```

#### Response:

```json
{
  "access": "new-jwt-access-token"
}
```

---

## 👤 User Profile

### 🔍 Get / Update Profile

**GET / PUT** `/profile/`\
Requires Authorization header:\
`Authorization: Bearer <access_token>`

#### Response (GET):

```json
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "role": "user"
}
```

---

## 📦 Orders

### 🚚 Create Order

**POST** `/orders/`

#### Request Body:

```json
{
  "pickup_address": "123 Main St",
  "delivery_address": "456 Elm St",
  "package_details": "Books",
  "total_amount": "20.00",
  "delivery_man_id": 3,
  "pay_now": true
}
```

#### Response:

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Order created successfully",
  "Data": {
    "id": 1,
    "pickup_address": "..."
  },
  "client_secret": "stripe-client-secret"
}
```

---

### 📜 View All My Orders (User)

**GET** `/orders/status/`

---

### 📜 Admin View All Orders

**GET** `/orders/`

---

### 🛠️ Update Order Status (Delivery Man)

**PUT** `/orders/{id}/`\
Only delivery man assigned to the order can update its status.

#### Request Body:

```json
{
  "status": "delivered"
}
```

---

### 💳 Pay for an Order (Stripe)

**POST** `/orders/{order_id}/pay/`

#### Response:

```json
{
  "client_secret": "stripe-payment-intent-client-secret"
}
```

---

## 👥 User Management (Admin Only)

### 📋 List All Users

**GET** `/users/`

### 📘 Create User

**POST** `/users/`

### 🔍 Retrieve / Update / Delete User

**GET / PUT / DELETE** `/users/{id}/`

---



## 📬 Postman Collection

Include a file named courier_api_postman_collection.json containing:

- All request endpoints
- Example bodies
- Sample responses
- Variables for BaseURL and tokens

You can export from Postman via: File → Export → Collection v2.1

## 🙋‍♂️ Roles
| Role        | Permissions                         |
| ----------- | ----------------------------------- |
| Admin       | Manage users and orders             |
| User        | Create and pay for orders           |
| DeliveryMan | View assigned orders, update status |

## 📩 Contact
For questions or feedback, feel free to open an issue or contact [shadia2169@gmail.com].


