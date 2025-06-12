# E-Commerce Backend (FastAPI)

## 🌐 Project Overview

This project is a RESTful backend API for an e-commerce platform built with **FastAPI**,  **SQLAlchemy**, **JWT authentication**, and **role-based access control (RBAC)**. 
It supports full admin product management, secure user authentication, product exploration, cart handling, and a dummy checkout flow.



## Features

- User & Admin registration/login
- JWT-based authentication (Access tokens)
- Product CRUD (Admin only)
- Cart management (User)
- Checkout system
- Order management (User)
- Role-based access control using dependencies
- Swagger UI 


## Tech Stack

- **Python**
- **Framework**
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Database**: SQLite
- **Authentication**: JWT


## 📂 Project Structure

```
app/
├── main.py                # Entry point
├── auth/                 # Authentication logic
│   ├── routes.py         # Signup, Signin, Reset Password APIs
│   ├── models.py         # User model
│   ├── utils.py          # Password hashing, token generation
├── products/             # Product CRUD
├── cart/                 # Cart operations
├── checkout/             # Checkout logic
├── orders/               # Order models and history
├── core/                 # Config, DB setup, logger
├── middlewares/          # (Optional) Custom middlewares
├── utils/                # Shared helpers
├── tests/                # (Optional) Manual/API test files


```


## 🚀 Setup Instructions

Follow the steps below to get the application up and running:

1. **Clone the repository**:

```bash
git clone https://github.com/garima-savdekar/ECommerce-Backend.git
cd <repo-folder>
```

2. **Create and activate a virtual environment**:

```bash
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. **Install the dependencies**:

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file**:
   Include essential environment variables:

```ini
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key
SMTP_SERVER=smtp.example.com
EMAIL_FROM=your@email.com
EMAIL_PASSWORD=your-email-password
```

5. **Run the development server**:

```bash
uvicorn app.main:app --reload
```

## 🔍 API Documentation

Once the server is running, visit:

* **Swagger UI**: http://127.0.0.1:8000/docs
* **ReDoc**: http://127.0.0.1:8000/redoc

