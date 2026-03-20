# BudgetWise Travel Intelligence API

## Overview

**BudgetWise Travel Intelligence API** is a **data-driven RESTful API** designed to help users discover travel destinations based on:

* Budget constraints
* Weather preferences
* Country and city insights
* User-generated reviews

The system provides both **CRUD operations** and  **analytics-based endpoints** , making it a powerful backend service for travel planning applications.

👉 A **React frontend dashboard** is built as a **client application** that consumes this API:
[https://budgetwise-two.vercel.app/](https://budgetwise-two.vercel.app/)

👉 API Documentation (Swagger):
[https://budgetwise-api-6tzv.onrender.com/docs#/](https://budgetwise-api-6tzv.onrender.com/docs#/)

---

# Core Features

## Authentication

* JWT-based login system
* Role-based access (Admin / User)
* Protected routes for secure operations

---

## Countries & Cities

* Full CRUD operations
* Retrieve cities by country
* Structured relational data

---

## Weather Data

* Access weather information per city
* Supports travel decision-making

---

## Travel Costs

* Estimated daily spending per destination
* Useful for budget planning

---

## Tourism Insights

* Tourist statistics per country
* Popularity indicators

---

## Reviews System

* Users can:
  * Submit reviews
  * Rate destinations
  * Share travel experiences

---

## Advanced API Endpoints

* Destination summaries
* City comparison
* Travel recommendations

---

# Technology Stack

* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Authentication:** JWT
* **Testing:** Pytest

---

# API Architecture & Structure

```id=
app/
 ├── main.py        → API entry point (initialises FastAPI, registers routes)
 ├── database.py    → Database configuration (engine, session, Base)
 ├── models/        → ORM models (database tables: Country, City, Review)
 ├── schemas/       → Data validation (request & response models)
 ├── routers/       → API endpoints grouped by feature (cities, countries, etc.)
 ├── auth/          → Authentication logic (JWT, login, permissions)
 └── tests/         → Automated tests (auth, endpoints, security)
```

---

## Architecture Explanation

The system follows a  **layered architecture** :

* **Routers Layer** → Handles HTTP requests (API endpoints)
* **Schemas Layer** → Validates incoming/outgoing data
* **Models Layer** → Represents database structure
* **Database Layer** → Manages data persistence

This separation ensures:

* Maintainability
* Scalability
* Clean code organisation

---

# ⚙️ Running the API Locally

```bash
git clone https://github.com/Mondr23/BudgetWise-api.git

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

📍 API runs on:
[http://127.0.0.1:8000](http://127.0.0.1:8000/)

📄 Documentation:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

# Testing

```bash
pytest
```

Includes:

* Authentication tests
* Authorization tests
* Endpoint validation

---

# Example API Endpoints

```id=
GET /cities/
GET /cities/{id}
POST /cities/
PUT /cities/{id}
DELETE /cities/{id}

GET /weather/{city_id}
GET /compare/cities
POST /reviews/
```

---

# Frontend (Client Application)

**Features**

* View travel costs
* Add & view reviews
* Compare destinations
* API health monitoring

Frontend URL:
[https://budgetwise-two.vercel.app/](https://budgetwise-two.vercel.app/)

---

## Tech Stack

* React (Vite)
* Three.js + React Three Fiber
* React Icons
* Fetch API

---

## **Run Frontend Locally**

```
git clone https://github.com/Mondr23/BudgetWise-api.git
cd travel-dashboard

npm install --legacy-peer-deps

npm run dev
```

📍 Runs on:
[http://localhost:5173](http://localhost:5173)

---

# Deployment

* **API (Backend):** Render
* **Frontend (Client):** Vercel
