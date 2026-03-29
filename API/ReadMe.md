# Profit Tracker (FastAPI + Vanilla JS)

This project is a simple, clean FastAPI backend paired with a lightweight frontend for tracking profits. It includes a REST API, a SQLite database, and a static web interface served directly by FastAPI.

---

## 🚀 Features
- Add, view, update, and delete profit entries  
- FastAPI backend with organized routes and CRUD logic  
- SQLite database with SQLAlchemy  
- Simple frontend using HTML, CSS, and JavaScript  
- Fully self‑contained — no external services required  

---

## 📁 Project Structure

project/
├── main.py
├── api/
│    ├── init.py
│    ├── database.py
│    ├── schemas.py
│    ├── crud.py
│    └── profit_routes.py
│
├── web/
│    ├── profit.html
│    ├── css/
│    │    └── profit.css
│    ├── js/
│    │    └── profit.js
│    └── images/
│         └── (optional)
│
├── requirements.txt
├── README.md
└── .gitignore
---

## 🛠️ Installation

### 1. Create a virtual environment (recommended)
python -m venv venv
Activate it:

- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 2. Install dependencies
pip install -r requirements.txt
---

## ▶️ Running the Server

Start FastAPI with Uvicorn:

uvicorn main:app --reload
The server will start at:

http://localhost:8000
---

## 🌐 Accessing the Frontend

Open your browser and go to:

http://localhost:8000/web/profit.html
This loads the profit tracker interface.

---

## 📡 API Endpoints

All API routes are prefixed with `/api`.

Example:
- `GET /api/profits`
- `POST /api/profits`
- `PUT /api/profits/{id}`
- `DELETE /api/profits/{id}`

---

## 🧩 Notes
- The database file (`database.db`) will be created automatically on first run.
- You can safely delete any unused files from older repos — only the files listed above are required.

---

## 📜 License
This project is for educational and internal use.
