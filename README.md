# Health Info System

A full-stack Single Page Application (SPA) for managing clients and health programs/services. Doctors authenticate via API keys and can perform the following:

- **Create and manage health programs** (TB, Malaria, HIV, etc.)
- **Register new clients**
- **Enroll clients** in one or more programs
- **Search** for clients by name
- **View client profiles**, including their program enrollments
- **Admin Panel** for super-admins to onboard new doctors and email API keys

---

## 📁 Directory Structure

```
/server                           # Flask backend
├── app
│   ├── __init__.py               # App factory
│   ├── config.py                 # Configuration classes
│   ├── models.py                 # SQLAlchemy models
│   ├── routes
│   │   ├── auth.py               # /api/auth routes
│   │   ├── clients.py            # /api/clients routes
│   │   ├── programs.py           # /api/programs routes
│   │   └── enrollments.py        # /api/enrollments routes
│   └── utils
│       └── auth.py               # Decorators: api_key_required, super_admin_required
├── migrations/                   # Alembic migrations
├── seed.py                       # Bootstrap initial super-admin + API key
├── run.py                        # Entrypoint
└── Pipfile                       # Dependencies

/frontend                         # React (Vite) Frontend
├── src
│   ├── App.jsx                   # Main router & layout
│   ├── main.jsx                  # ReactDOM render
│   ├── components
│   │   ├── LandingPage.jsx       # Welcome page
│   │   ├── ApiKeyPrompt.jsx      # API key entry & validation
│   │   ├── RegisterClient.jsx    # Client registration form
│   │   ├── SearchClients.jsx     # Search form & results
│   │   ├── ViewClientProfile.jsx # Profile lookup & display
│   │   ├── CreateProgram.jsx     # Program creation form
│   │   ├── EnrollClient.jsx      # Enrollment form with program list
│   │   └── AdminPanel.jsx        # Super-admin doctor provisioning
├── vite.config.js                # Dev server proxy
└── package.json                  # Dependencies & scripts
```

---

## 🚀 Features

- **API First**: All functionality exposed via RESTful endpoints secured by API keys.
- **API Key Authentication**: `api_key_required` decorator enforces valid key in `X-API-KEY` header.
- **Super-Admin Role**: `super_admin_required` decorator for provisioning new doctors.
- **Frontend**:
  - React + Vite for fast HMR
  - Tailwind CSS for styling
  - React Router for SPA navigation

---

## ⚙️ Backend Setup

1. **Clone and install**:
    ```bash
    git clone <repo-url>
    cd server
    pipenv install --dev
    pipenv shell
    ```

2. **Environment Variables**: Create a `.env` in `/server`:
    ```ini
    DATABASE_URL=postgresql://user:pass@localhost/health_db
    MAIL_USERNAME=<your gmail>
    MAIL_PASSWORD=<app-password>
    ```

3. **Database Migrations**:
    ```bash
    flask db init         # only first time
    flask db migrate -m "Initial"
    flask db upgrade
    ```

4. **Seed Super-Admin**:
    ```bash
    python seed.py
    # Outputs: doctor & API key in console.
    ```

5. **Run Server**:
    ```bash
    flask run
    ```
    - API served at `http://localhost:5000/api/...`

---

## 🔑 API Endpoints

### Auth
- `GET /api/auth/validate` &nbsp;&nbsp;Validate API key → returns `{ doctor: { id, name, email, is_admin } }`

### Clients
- `POST /api/clients/register` &nbsp;Register a client
- `GET /api/clients/` &nbsp;List all clients
- `GET /api/clients/search?q=` &nbsp;Search clients by name
- `GET /api/clients/:id` &nbsp;Get client profile and enrollments

### Programs
- `POST /api/programs/` &nbsp;Create program
- `GET /api/programs/` &nbsp;List programs
- `GET /api/programs/list` &nbsp;(for dropdown) returns `{ id, name, description, created_at }`

### Enrollments
- `POST /api/enrollments/:client_id` &nbsp;Enroll in programs via `{ program_ids: [1,2] }`

### Admin (super-admin only)
- `POST /api/admin/doctors` &nbsp;Create doctor & email API key
- `POST /api/admin/doctors/:id/key` &nbsp;Rotate doctor’s API key

_All endpoints require `X-API-KEY` header except the seed script._

---

## 🌐 Frontend Setup

1. **Navigate & install**:
    ```bash
    cd frontend
    npm install
    ```

2. **Configure proxy** in `vite.config.js`:
    ```js
    server: {
      proxy: {
        '/api': 'http://localhost:5000'
      }
    }
    ```

3. **Run dev server**:
    ```bash
    npm run dev
    ```
    - App at `http://localhost:5173`

4. **Workflow**:
    - **Landing Page** → **Get Started**
    - **Paste API Key** → **Verify**
    - **Portal** with navigation cards:
        - Register Client
        - Search Clients
        - View Client Profile
        - Create Program
        - Enroll Client (checkbox dropdown)
        - Admin Panel (if `is_admin`)

---

## 📚 Technologies

- **Backend**: Python, Flask, SQLAlchemy, Flask-Migrate, Flask-Mail, PostgreSQL
- **Frontend**: React, Vite, React Router, Tailwind CSS

---

## ✅ Contributing

PRs welcome! Please follow these guidelines:
- Write clean, well-documented code.
- Add tests for new features.
- Update migrations and seed scripts as needed.

---

## 📄 License

MIT © Your Name

