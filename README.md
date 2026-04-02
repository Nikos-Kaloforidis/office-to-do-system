# Office To-Do Management System

## Project Description

The Office To-Do System is a practical, full-stack application built to help small to mid-sized teams organize their internal tasks. It moves away from simple, unorganized lists by requiring every task to be linked to a specific user and every user to belong to a department.

### How it Works

The project is built using a standard three-tier architecture:

- **Backend:** A FastAPI server handles the business logic. It uses synchronous (blocking) execution, which was chosen for its reliability and straightforward debugging in a standard office CRUD environment.
- **Frontend:** A multi-page Streamlit interface. Instead of one long script, the UI is broken down into logical sections like an Admin Panel for setup and a MyDepartment page for team-specific viewing.
- **Database:** A PostgreSQL instance stores the data. We use SQLAlchemy to interact with the database, which allows us to define our tables as Python classes.

### Practical Features

- **Predictable Security:** Authentication is handled via JWT (JSON Web Tokens). When a user logs in, they get a token that the frontend stores and sends back with every request to verify who is asking for data.
- **Clean Data Flow:** Every piece of data entering or leaving the API is filtered through Pydantic schemas. This prevents the database from being cluttered with malformed data and ensures the frontend always knows what kind of response to expect.
- **Layered Logic:** To keep the code manageable, database queries are kept in a "CRUD" layer, separate from the API endpoints. This makes it easier to update how data is saved without breaking the actual web routes.
- **Automatic Setup:** The system includes a seeding routine. On the first run, it automatically creates a "Management" department and a default admin user, so you don't have to manually interact with the database just to log in for the first time.

### Intended Use

## This tool is designed for an environment where one person (an Admin) sets the structure. After the Admin creates the departments and the initial user accounts, team members can log in, manage their profiles, and track their assigned work in a private, authenticated space.

## 📊 System Overview

| Component    | Technology     | Role                                    |
| :----------- | :------------- | :-------------------------------------- |
| **Frontend** | Streamlit      | Reactive UI & Data Visualization        |
| **API**      | FastAPI        | Asynchronous Logic & JWT Authentication |
| **Database** | PostgreSQL 16  | Relational Storage & Data Integrity     |
| **Auth**     | Argon2 / JWT   | Industry-standard Security & Hashing    |
| **DevOps**   | Docker Compose | Service Orchestration & Networking      |

---

## 📂 Project Structure

```text
office-todo-project/
├── app/ # 🧠 BACKEND SERVICE (FastAPI)
│ ├── auth/ # Security: JWT generation & Token verification
│ ├── core/ # Global Settings: App config & Environment vars
│ ├── crud/ # Logic: Create, Read, Update, Delete database operations
│ ├── models/ # Database: SQLAlchemy ORM table definitions
│ ├── schemas/ # Validation: Pydantic models for request/response data
│ ├── database.py # Engine: Connection pooling & Session management
│ └── main.py # Entry: FastAPI application boot & lifespan seeding
├── frontend/ # 🖥️ FRONTEND SERVICE (Streamlit)
│ ├── .streamlit/ # UI Configuration: Themes and server settings
│ ├── pages/ # Multi-page Navigation: Admin, Dept, and Profile UI
│ ├── utils/ # Helpers: API clients and notification components
│ └── Home.py # Entry: Main landing page for the Streamlit dashboard
├── tests/ # 🧪 QUALITY ASSURANCE
│ ├── conftest.py # Test Configuration: Sets up isolated test databases
│ └── test\*\*.py # Automated test suites for all API endpoints
├── backend.Dockerfile # Build instructions for the Python Backend
├── frontend.Dockerfile # Build instructions for the Streamlit Frontend
├── docker-compose.yaml # Orchestration: Connects DB, Backend, and Frontend
├── pyproject.toml # Dependency Management: Standard package configuration
└── README.md # Documentation: Setup guide and project scope
```

# 🚀 Getting Started Guide

Follow these steps to initialize the Office To-Do environment on your local machine.

---

### 1. Prerequisites

Ensure you have the following installed on your host system:

- **Docker Desktop** (or Docker Engine + Compose V2)
- **Git** (to clone/manage the repository)

---

### 2. Environment Configuration

Create a .env file in the root directory. While Docker provides defaults, ensure your local environment aligns with these keys:

- **DATABASE_URL**

- **TEST_DATABASE_URL**
-
- **SECRET_KEY (A random string for JWT)**

### 2. Launch the Infrastructure

Navigate to the project root directory and execute the build command. This will download the necessary images, create the private network, and set up the persistent volumes.

```bash
docker compose up -d --build
```

### 3. Service Access Points

Once the containers report a **running** or **healthy** status, the following gateways are available for local development and management:

| Service               | Local Address                                            | Description                                                 |
| :-------------------- | :------------------------------------------------------- | :---------------------------------------------------------- |
| **User Dashboard**    | [http://localhost:8501](http://localhost:8501)           | Main Streamlit interface for daily task management.         |
| **API Documentation** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive Swagger UI for testing and exploring endpoints. |
| **Database Manager**  | [http://localhost:8080](http://localhost:8080)           | Adminer Web GUI for manual PostgreSQL table inspection.     |

---

### 4. Initial Authentication & Bootstrap

To ensure immediate usability, the system employs an automated **Lifespan Seeding** routine. On the very first successful database connection, the application initializes with a single administrative account.

**Default Administrative Credentials:**

- **Username:** `admin`
- **Password:** `admin`

**Post-Login Workflow:**

1. **Login:** Use the credentials above to access the Streamlit Dashboard.
2. **Setup:** Once authenticated as the admin, you gain full permissions to use the interface to:
   - Create new **Departments** (required before adding users).
   - Register new **Users** and assign them to specific departments.
   - Initialize and assign **Tasks**.

> **Adminer Connection Note:** If accessing the database directly via port 8080, use `db` as the server hostname, `admin` as the username/password, and `officeToDo` as the database name.

### 5. System Verification

To confirm that the backend has successfully initialized the schema and connected to the PostgreSQL instance, use the following diagnostic commands:

**Check Container Status:**

```bash
docker compose ps
```

**Stream Backend Initialization Logs:**

```bash
docker compose logs -f backend
```

---

### 6. Maintenance & Testing

**Running Automated Tests:**
Verify the API and Auth logic:

```bash
docker compose exec backend pytest
```

**Applying Database Migrations:**
If you update the models, apply changes via Alembic:

```bash
docker compose exec backend alembic upgrade head
```

**Wiping Data & Re-seeding:**
To reset the database to its original "Admin only" state:

```bash
docker compose down -v
docker compose up -d
```

---

### 7. Shutdown Procedure

To halt all services while preserving the current state of your database:

```bash
docker compose stop
```

To fully remove the containers, the private network, and the associated images:

```bash
docker compose down --rmi all
```
