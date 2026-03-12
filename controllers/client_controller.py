from flask import Blueprint, render_template, request, redirect
from database import get_db
from services.client_service import generate_client_code
import re

client_routes = Blueprint('clients', __name__)

def validate_email(email):
    """Validate email format server-side"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@client_routes.route("/")
def list_clients():

    db = get_db()

    try:
        clients = db.execute("""
        SELECT c.id, c.name, c.client_code,
        COUNT(cc.contact_id) as contacts
        FROM clients c
        LEFT JOIN client_contacts cc
        ON c.id = cc.client_id
        GROUP BY c.id
        ORDER BY c.name ASC
        """).fetchall()

        return render_template("clients.html", clients=clients)
    finally:
        db.close()

@client_routes.route("/create",methods=["POST"])
def create():

    name = request.form["name"]

    if not name:
        return "Name required",400

    db = get_db()

    code = generate_client_code(name,db)

    db.execute(
        "INSERT INTO clients(name,client_code) VALUES (?,?)",
        (name,code)
    )

    db.commit()

    return redirect("/")

@client_routes.route("/client/<int:client_id>")
def view_client(client_id):

    db = get_db()

    try:
        # Get client info
        client = db.execute("SELECT id, name, client_code FROM clients WHERE id = ?", (client_id,)).fetchone()

        if not client:
            return "Client not found", 404

        # Get linked contacts ordered by full name
        contacts = db.execute("""
            SELECT c.id, c.surname || ' ' || c.name AS fullname, c.email
            FROM contacts c
            INNER JOIN client_contacts cc ON c.id = cc.contact_id
            WHERE cc.client_id = ?
            ORDER BY c.surname ASC, c.name ASC
        """, (client_id,)).fetchall()

        return render_template("client_view.html", client=client, contacts=contacts)
    finally:
        db.close()

@client_routes.route("/client/<int:client_id>/link-contact")
def link_contact_form(client_id):

    db = get_db()

    try:
        # Get client info
        client = db.execute("SELECT id, name, client_code FROM clients WHERE id = ?", (client_id,)).fetchone()

        if not client:
            return "Client not found", 404

        return render_template("link_contact.html", client=client)
    finally:
        db.close()

@client_routes.route("/client/<int:client_id>/link-contact", methods=["POST"])
def link_contact(client_id):

    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")

    if not all([name, surname, email]):
        return "All fields are required", 400

    if not validate_email(email):
        return "Invalid email format", 400

    db = get_db()

    try:
        # Check if client exists
        client = db.execute("SELECT id FROM clients WHERE id = ?", (client_id,)).fetchone()
        if not client:
            return "Client not found", 404

        # Check if contact already exists by email
        existing_contact = db.execute(
            "SELECT id FROM contacts WHERE email = ?",
            (email,)
        ).fetchone()

        if existing_contact:
            contact_id = existing_contact['id']
        else:
            # Create new contact
            cursor = db.execute(
                "INSERT INTO contacts (name, surname, email) VALUES (?, ?, ?)",
                (name, surname, email)
            )
            contact_id = cursor.lastrowid
            db.commit()  # Commit the contact creation

        # Check if link already exists
        existing_link = db.execute(
            "SELECT client_id FROM client_contacts WHERE client_id = ? AND contact_id = ?",
            (client_id, contact_id)
        ).fetchone()

        if not existing_link:
            # Create the link
            db.execute(
                "INSERT INTO client_contacts (client_id, contact_id) VALUES (?, ?)",
                (client_id, contact_id)
            )
            db.commit()  # Commit the link creation

        return redirect(f"/client/{client_id}")

    except Exception as e:
        db.rollback()  # Rollback on error
        return f"Error linking contact: {str(e)}", 500
    finally:
        db.close()  # Always close the connection