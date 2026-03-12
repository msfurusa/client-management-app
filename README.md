# client-management-app

Client & Contact Management System

Overview

A small Flask-based application to manage Clients and Contacts with a many-to-many relationship. Supports creating and listing clients and contacts, linking/unlinking contacts to clients, and server-side validation (unique email and email format).

Features

- Clients: create (auto-generated code), list, link/unlink contacts
- Contacts: create/edit, email validation & uniqueness, list, link/unlink clients
- Database: SQLite with normalized schema and many-to-many relationship via `client_contacts`
- UI: Simple HTML templates with tabs and AJAX unlink support

Prerequisites

- Python 3.10+ (tested with 3.14)
- Git

Setup

1. Clone the repository
   git clone "client-management-app"
2. Enter the project directory
   cd client-management-app
3. Create and activate a virtual environment
   python3 -m venv .venv
   source .venv/bin/activate
4. Install dependencies
   pip install -r requirements.txt

Note: `requirements.txt` is present in the repository. To regenerate it from your virtual environment:

   source .venv/bin/activate
   python -m pip freeze > requirements.txt

Database

- The app uses SQLite (database.db). To recreate/reset the database:

   rm -f database.db
   sqlite3 database.db < schema.sql

Running the app

1. Activate the virtual environment
   source .venv/bin/activate
2. Start the Flask server
   python3 app.py
3. Open http://127.0.0.1:5000/ in your browser

Project structure

- app.py - Flask application entrypoint
- controllers/ - Flask blueprints (clients, contacts)
- services/ - Business logic (client_service, contact_service)
- templates/ - Jinja2 HTML templates
- static/ - CSS and JavaScript assets
- database.py - DB helper
- schema.sql - Database schema
- requirements.txt - Python dependencies

Development notes

- Contact templates: templates/contacts.html and templates/contact_form.html
- Client templates: templates/clients.html and templates/client_view.html
- To reset the database, run the commands in the Database section above

License
