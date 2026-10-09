# Expense Tracker API

A REST API built with FastAPI. Users can register, log in to get a JWT token,
and manage their own expenses (create, read, update, delete).
Each user can only see and change their own expenses.

## Expense fields

| Field | Description |
| --- | --- |
| id | Unique number, set by the database |
| title | Name of the expense (required) |
| description | Extra details (optional) |
| amount | Money spent, must be greater than 0 |
| category | food, transport, rent, utilities, entertainment, health, shopping or other |
| expense_date | Date of the expense, defaults to today |
| created_at | Time the record was created |
| user_id | The owner of the expense |

## Tech used

- Python, FastAPI, Uvicorn
- SQLAlchemy with SQLite
- Pydantic for validation
- PyJWT for tokens
- pwdlib (Argon2) for password hashing

## How to run

1. Clone the project:
```
   git clone https://github.com/mubinaparveen1706-arch/expense-tracker-api.git
   cd expense-tracker-api
```
2. Create and activate a virtual environment:
```
   python -m venv .venv
   .venv\Scripts\activate
```
   (On Mac/Linux use `source .venv/bin/activate`)
3. Install the packages:
```
   pip install -r requirements.txt
```
4. Create your `.env` file by copying `.env.example`:
```
   copy .env.example .env
```
   (On Mac/Linux use `cp .env.example .env`)
5. Put a real secret key in `.env`. Generate one with:
```
   python -c "import secrets; print(secrets.token_hex(32))"
```
6. Start the server:
```
   uvicorn app.main:app --reload
```
7. Open http://127.0.0.1:8000/docs in your browser.

## Environment variables

| Name | Description |
| --- | --- |
| SECRET_KEY | Secret used to sign tokens (required) |
| ALGORITHM | Token algorithm, HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | How long a token lasts, 30 |
| DATABASE_URL | Database location, sqlite:///./expenses.db |

## Endpoints

| Method | Route | Login needed | What it does |
| --- | --- | --- | --- |
| POST | /auth/register | No | Create a new user |
| POST | /auth/login | No | Get a JWT token |
| GET | /auth/me | Yes | Show the logged-in user |
| POST | /expenses | Yes | Create an expense |
| GET | /expenses | Yes | List your expenses (skip, limit, category) |
| GET | /expenses/{id} | Yes | Get one expense |
| PUT | /expenses/{id} | Yes | Replace an expense |
| PATCH | /expenses/{id} | Yes | Update part of an expense |
| DELETE | /expenses/{id} | Yes | Delete an expense |

## How to use it in Swagger

1. Go to `/docs`.
2. Use `POST /auth/register` to create a user.
3. Click **Authorize**, enter your email as the username and your password.
4. Try the `/expenses` routes.

## Security

- Passwords are hashed, never stored as plain text.
- Tokens expire after 30 minutes.
- Invalid or missing tokens return 401.
- Another user's expense returns 404.
- The real `.env` file is not uploaded to GitHub.