from flask import Blueprint, render_template, jsonify, request, redirect
from database import get_db
from services.contact_service import (
    validate_email, get_all_contacts, get_contact_by_id,
    get_linked_clients, create_contact, update_contact,
    link_contact_to_client, unlink_contact_from_client,
    contact_email_exists
)

contact_routes = Blueprint('contacts', __name__)

@contact_routes.route("/contacts")
def list_contacts():
    db = get_db()
    
    try:
        contacts = get_all_contacts(db)
        return render_template("contacts.html", contacts=contacts)
    finally:
        db.close()

@contact_routes.route("/contacts/create", methods=["GET"])
def create_contact_form():
    return render_template("contact_form.html", contact=None)

@contact_routes.route("/contacts/create", methods=["POST"])
def create_new_contact():
    name = request.form.get("name", "").strip()
    surname = request.form.get("surname", "").strip()
    email = request.form.get("email", "").strip()
    
    if not all([name, surname, email]):
        return "All fields are required", 400
    
    if not validate_email(email):
        return "Invalid email format", 400
    
    db = get_db()
    
    try:
        if contact_email_exists(db, email):
            return "Email already exists", 400
        
        contact_id = create_contact(db, name, surname, email)
        return redirect(f"/contacts/{contact_id}")
    except Exception as e:
        db.rollback()
        return f"Error creating contact: {str(e)}", 500
    finally:
        db.close()

@contact_routes.route("/contacts/<int:contact_id>", methods=["GET"])
def view_contact(contact_id):
    db = get_db()
    
    try:
        contact = get_contact_by_id(db, contact_id)
        
        if not contact:
            return "Contact not found", 404
        
        linked_clients = get_linked_clients(db, contact_id)
        
        # Get all available clients to link
        all_clients = db.execute("""
            SELECT id, name, client_code
            FROM clients
            ORDER BY name ASC
        """).fetchall()
        
        return render_template("contact_form.html", contact=contact, linked_clients=linked_clients, all_clients=all_clients)
    finally:
        db.close()

@contact_routes.route("/contacts/<int:contact_id>", methods=["POST"])
def update_contact_details(contact_id):
    name = request.form.get("name", "").strip()
    surname = request.form.get("surname", "").strip()
    email = request.form.get("email", "").strip()
    
    if not all([name, surname, email]):
        return "All fields are required", 400
    
    if not validate_email(email):
        return "Invalid email format", 400
    
    db = get_db()
    
    try:
        contact = get_contact_by_id(db, contact_id)
        
        if not contact:
            return "Contact not found", 404
        
        # Check if email is already used by another contact
        if email != contact['email'] and contact_email_exists(db, email, contact_id):
            return "Email already exists", 400
        
        update_contact(db, contact_id, name, surname, email)
        return redirect(f"/contacts/{contact_id}")
    except Exception as e:
        db.rollback()
        return f"Error updating contact: {str(e)}", 500
    finally:
        db.close()

@contact_routes.route("/contacts/<int:contact_id>/link-client", methods=["POST"])
def link_client_to_contact(contact_id):
    client_id = request.form.get("client_id")
    
    if not client_id:
        return "Client ID required", 400
    
    db = get_db()
    
    try:
        contact = get_contact_by_id(db, contact_id)
        if not contact:
            return "Contact not found", 404
        
        # Check if client exists
        client = db.execute("SELECT id FROM clients WHERE id = ?", (client_id,)).fetchone()
        if not client:
            return "Client not found", 404
        
        link_contact_to_client(db, contact_id, client_id)
        return redirect(f"/contacts/{contact_id}")
    except Exception as e:
        db.rollback()
        return f"Error linking client: {str(e)}", 500
    finally:
        db.close()

@contact_routes.route("/contacts/<int:contact_id>/unlink/<int:client_id>", methods=["POST"])
def unlink_client_from_contact(contact_id, client_id):
    db = get_db()
    
    try:
        unlink_contact_from_client(db, contact_id, client_id)
        return redirect(f"/contacts/{contact_id}")
    except Exception as e:
        db.rollback()
        return f"Error unlinking client: {str(e)}", 500
    finally:
        db.close()

@contact_routes.route("/contacts/<int:contact_id>/unlink/<int:client_id>", methods=["DELETE"])
def ajax_unlink_client(contact_id, client_id):
    db = get_db()
    
    try:
        unlink_contact_from_client(db, contact_id, client_id)
        return jsonify({"status": "ok"})
    finally:
        db.close()