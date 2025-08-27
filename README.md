# fastapi-task-api
Task Management API  1.0.0  OAS 3.1 /openapi.json A simple, documented REST API with FastAPI, SQLite, SQLAlchemy, and JWT auth.
# 🚀 FastAPI Task Management API

A simple, documented **REST API** built with **FastAPI**, **SQLite**, **SQLAlchemy**, and **JWT authentication**.  
It supports full CRUD operations for managing tasks with authentication and token-based access.

---

## 📌 Features
- 🔑 User Authentication (Signup & Login with JWT)
- ✅ Task CRUD API (Create, Read, Update, Delete)
- 🛡️ Protected Routes (only logged-in users can access tasks)
- 📖 Interactive API Docs with Swagger UI (`/docs`) and ReDoc (`/redoc`)
- 🗄️ SQLite Database with SQLAlchemy ORM
- 🐳 Dockerized for easy deployment

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Kittu268/fastapi-task-api.git
cd fastapi-task-api
2️⃣ Create virtual environment & install dependencies
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
3️⃣ Run the application
uvicorn main:app --reload
4️⃣ Access the API
Swagger UI → http://127.0.0.1:8000/docs
ReDoc → http://127.0.0.1:8000/redoc

Authentication

Signup: POST /auth/signup

Login: POST /auth/login → Returns a JWT access_token

Use Authorize button in Swagger UI → enter Bearer <your_token>

➕ Create Task
GET /tasks
Authorization: Bearer <your_token>
✏️ Update Task
PUT /tasks/{task_id}
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "title": "Updated Task Title",
  "description": "Updated Task Description",
  "completed": true
}

❌ Delete Task
DELETE /tasks/{task_id}
Authorization: Bearer <your_token>

🐳 Docker Setup
# Build Docker image
docker build -t fastapi-task-api .

# Run container
docker run -d -p 8000:8000 fastapi-task-api
Project Structure
├── main.py                 # FastAPI app entry point
├── models.py               # SQLAlchemy models
├── database.py             # DB setup (SQLite)
├── auth.py                 # Authentication & JWT
├── crud.py                 # CRUD operations
├── schemas.py              # Pydantic schemas
├── tasks.db                # SQLite database
├── requirements.txt        # Dependencies
├── Dockerfile              # Docker setup
├── postman_collection.json # API testing collection
└── README.md               # Documentation
📜 License

MIT License © 2025 https://github.com/Kittu268


