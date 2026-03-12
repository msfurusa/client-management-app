# client-management-app

Client & Contact Management System

## Overview
This is a small Flask-based application to manage Clients and Contacts with a many-to-many relationship. It supports creating and listing clients and contacts, linking/unlinking contacts to clients, and basic validation (unique email and email format).

## Features
- Clients
  - Create client with auto-generated client code
  - List clients and count linked contacts
  - Link/unlink contacts
- Contacts
  - Create contact
  - Server-side email validation and uniqueness enforcement
  - List contacts and count linked clients
  - Link/unlink clients to contacts
- Database
  - SQLite with normalized schema and many-to-many relationship via `client_contacts`
  - Indexes for performance
- UI
  - Simple HTML templates with tabs and AJAX unlink support

## Prerequisites
- Python 3.10+ (tested with 3.14)
- Git

## Setup
1. Clone the repository
   git clone https://github.com/msfurusa/client-management-app.git
2. Create and activate virtual environment
   python3 -m venv .venv
   source .venv/bin/activate
3. Install dependencies
   pip install -r requirements.txt

Note: If `requirements.txt` is not present, install Flask manually:
   pip install flask

## Running the app
1. Activate the virtual environment
   source .venv/bin/activate
2. Start the Flask server
   python3 app.py
3. Open http://127.0.0.1:5000/ in your browser

## Project Structure
- app.py - Flask app entrypoint
- controllers/ - Flask blueprints for Clients and Contacts
- services/ - Business logic helpers (client_service, contact_service)
- templates/ - Jinja2 templates for UI
- static/ - Styles and JavaScript
- database.py - SQLite helper to get DB connection
- schema.sql - DB schema

## Development notes
- Contacts: templates/contacts.html and templates/contact_form.html
- Clients: templates/clients.html and templates/client_view.html
- To reset DB: drop database.db and re-run schema.sql

## Contributing
Contributions welcome. Please open issues or pull requests.

## License
MIT (placeholder)
