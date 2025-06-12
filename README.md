# E-commerce Backend API using FastAPI

A robust, secure, and modular RESTful API for an e-commerce platform developed using FastAPI. This backend supports authentication, admin product management, user browsing, cart management, order processing, and more.

---

## Features

 -**Authentication**: Supports Signup, Signin, and Forgot/Reset Password. When a user forgets their password, a secure reset token is sent via email. Implements JWT access and refresh tokens and role-based access control (Admin/User) for secure API access.

 -**Product Management**: Admins can create, read, update, and delete products. Public users can browse, search, filter, and paginate through product listings.

 -**Cart System**: Logged-in users can add, remove, update, and view items in their personal cart.

 -**Checkout & Orders**: Includes a dummy checkout that clears the cart and creates orders. Users can view their order history and detailed order info.

 -**Security & Enhancements**: Uses bcrypt for password hashing and JWT for session handling. Validates input with Pydantic, logs all key events, and handles errors with a consistent JSON format.

---

## Project Structure

```
ecommerce_backend/
├──alembic
├──app/ 
│   ├── main.py 
│   ├── __init__.py 
│   ├── auth/ 
│   │   ├── __init__.py
│   │   ├── models.py 
│   │   ├── utils.py 
│   │   ├── schemas.py 
│   │   ├── email_utils.py 
│   │   ├── routes.py  
│   ├── products/ 
│   │   ├── __init__.py
│   │   ├── models.py 
│   │   ├── schemas.py 
│   │   ├── routes.py  
│   │   ├── public_routes.py
│   ├── cart/ 
│   │   ├── __init__.py
│   │   ├── models.py 
│   │   ├── schemas.py 
│   │   ├── routes.py 
│   ├── checkout/ 
│   │   ├── __init__.py 
│   │   ├── routes.py 
│   ├── orders/ 
│   │   ├── __init__.py 
│   │   ├── routes.py 
│   │   ├── models.py 
│   │   ├── schemas.py 
│   ├── core/ 
│   │   ├── __init__.py 
│   │   ├── config.py 
│   │   ├── database.py 
│   ├── middlewares/ 
│   │   ├── __init__.py 
│   │   ├── logging_middleware.py
│   ├── utils/ 
│   │   ├── __init__.py 
│   │   ├── dependency.py 
├──logs
├──myvenv
├──.env
├──alembic.ini
├──ecommerce.db
├──requirements.txt
├──seed.py
├──README.md
```



---

## Tech Stack

 -**FastAPI** – High-performance, modern Python web framework for building APIs with async support.

 -**SQLite** – Lightweight, file-based relational database used for development and testing.

 -**SQLAlchemy** – SQL toolkit and ORM used for managing models and database interaction.

 -**Pydantic** – Data validation and settings management using Python type hints.

 -**JWT** – For implementing secure authentication using access and refresh tokens.

 -**Uvicorn**– Lightning-fast ASGI server used to serve FastAPI applications.

 -**Alembic** – Lightweight database migration tool used with SQLAlchemy for schema changes.

---

## API Overview (Endpoints)

### Authentication Endpoints

* `POST /auth/signup` – Allows users to register by providing name, email, password, and role.
* `POST /auth/signin` – Authenticates users and returns access + refresh JWT tokens.
* `POST /auth/forgot-password` – Sends a secure password reset token to the user's email.
* `POST /auth/reset-password` – Resets the user's password using the token received via email.
* `POST /auth/refresh` – Issues a new access token using a valid refresh token.

### Admin Product Management (Admin Only)

* `POST /admin/products` – Add a new product to the catalog.
* `GET /admin/products` – View all products (supports pagination).
* `GET /admin/products/{id}` – View specific product details.
* `PUT /admin/products/{id}` – Update an existing product.
* `DELETE /admin/products/{id}` – Remove a product from the catalog.

### Public Product APIs

* `GET /products` – Browse products with filtering (category, price), sorting, and pagination.
* `GET /products/search` – Search products by keyword.
* `GET /products/{id}` – View detailed information about a single product.

### Cart Endpoints (User Only)

* `POST /cart` – Add a product to the user's cart.
* `GET /cart` – View all items in the user's cart.
* `PUT /cart/{product_id}` – Update quantity of a specific item in the cart.
* `DELETE /cart/{product_id}` – Remove an item from the cart.

### Checkout

* `POST /checkout` – Simulates payment, creates an order, and clears the cart.

### Order Management
* `GET /orders` – View user's order history with summary data.
* `GET /orders/{order_id}` – View detailed information about a specific order.

---


## Setup Instructions:

### Prerequisites
- Python 3.10+
- pip
- Visual Studio Code
- Postman
- SQLiteStudio
- SMTP Email

## Installation:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/VaishnaviGoyal8989/ecommerce_backend.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd ecommerce_backend
   ```

3. **Create a virtual environment:**

   ```bash
   python3 -m venv myvenv
   ```

4. **Activate the virtual environment:**

   On Windows:

   ```bash
   myvenv\Scripts\activate
   ```

   On macOS and Linux:

   ```bash
   source myvenv/bin/activate
   ```

5. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

**Access the Swagger UI :**

   - Swagger UI: [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)

---
  


### Run the Project

```bash

uvicorn app.main:app --reload

```

---

The API will be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


---

## 📋 Logging

Logs are written to:

```
logs/app.log
```
---

## Future Enhancements

* Integration with real payment gateway
* Image uploads
* Frontend UI with React/Vue

---

## Contributing

Feel free to contribute to the project. Fork the repository, make changes, and submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).


---



