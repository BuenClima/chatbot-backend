# 🤖 Chatbot Backend (FastAPI)

Welcome to the **Chatbot Backend** built with **FastAPI**! This project demonstrates a high-performance, scalable, and robust backend API designed for chatbot functionality. It integrates a modern asynchronous architecture, secure authentication, and efficient database handling, making it a solid solution for various chatbot systems.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.2-green.svg)](https://fastapi.tiangolo.com/)

---

## 🚀 **Project Overview**

The **Chatbot Backend** is built using **FastAPI**, a modern Python web framework that delivers high performance and scalability. This backend is designed to handle chatbot requests, manage conversations, and efficiently interact with external services or APIs for natural language processing.

### **Key Features**:

- **FastAPI** for building a high-performance asynchronous API.
- **JWT-based authentication** for secure access to API endpoints.
- **PostgreSQL** database integration using **SQLAlchemy** for efficient data handling.
- **Alembic** for smooth database migrations.
- **Pydantic** for robust request/response data validation.
- **Asynchronous architecture** for non-blocking operations and faster response times.
- **Automated testing** with **pytest** to ensure code quality and reliability.

---

## 🛠 **Tech Stack**

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Pydantic
- **Testing**: Pytest
- **CI/CD**: GitHub Actions for automated testing and linting
- **Documentation**: Auto-generated OpenAPI/Swagger documentation

---

## 🚀 **Getting Started**

### **1. Clone the repository**

```bash
git clone https://github.com/BuenClima/chatbot-backend.git
cd chatbot-backend
```

### **2. Set up environment variables**

Create a `.env` file in the root directory with the following content:

```ini
DATABASE_URL=postgresql://username:password@db:5432/dbname
ACCESS_JWT_SECRET=your_secret_key
REFRESH_JWT_SECRET=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
```

### **3. Install dependencies**

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
# or venv\Scripts\activate  # For Windows
pip install -r requirements.txt
```

### **4. Run the application using Podman Compose**

This project uses **Podman Compose** to set up the FastAPI application along with a **PostgreSQL** database.

1. Ensure **Podman Compose** is installed.
2. Run the following command to start the services:

```bash
podman-compose up --build
```

## 🧪 **Running Tests**

To run the test suite using **pytest**, run:

```bash
pytest
```

## 📄 **API Documentation**

FastAPI automatically generates interactive API documentation. You can access the API documentation using:

- **Swagger UI**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc**: [http://localhost:8080/redoc](http://localhost:8080/redoc)

These tools provide an interactive interface to explore the API and its endpoints.

## 🚀 **Deployment with Podman**

To containerize and deploy this application using **Podman**, follow these steps:

### **1. Build the Podman image**:

```bash
podman build -t chatbot-backend .
```

### **2. Run the Podman container:**:

```bash
podman run -d -p 8080:8080 --env-file .env chatbot-backend
```

## ✨ **Key Highlights**

- **Asynchronous API**: Built with Python’s `async` and `await`, ensuring fast, non-blocking operations.
- **Secure Authentication**: Implements JWT-based authentication for API security.
- **Scalable Architecture**: Modular and scalable, with separate modules for routing, business logic, and database operations.
- **CI/CD Integration**: Fully integrated with GitHub Actions for automated testing and linting to ensure high-quality code.
- **Pydantic Validation**: Strong request and response validation using Pydantic, ensuring robust data integrity.

---

## 📄 **License**

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🧑‍💻 **Contact**

Feel free to explore and contribute to the project!

- **GitHub**: [BuenClima](https://github.com/BuenClima)
