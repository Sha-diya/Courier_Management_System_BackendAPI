# Courier Management System - Backend API

This is the backend REST API for a Courier Management System built with Django REST Framework and JWT authentication.

## 🌐 Live API

**Base URL:** https://courier-management-system-backendapi.onrender.com

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
For questions or feedback, feel free to open an issue or contact [shadia.akther.cse@gmail.com].

---

## ✅ To-Do for Hand-off

1. ✅ Push all code to GitHub
2. ✅ Create & add `README.md` file
3. ✅ Export Postman collection with all tested endpoints
4. ✅ Mention live API URL: `https://courier-management-system-backendapi.onrender.com`
5. ✅ Add instructions for setting up `.env` and Stripe key

---


