import re

def validate_email(email):
    """Validate email format server-side"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_all_contacts(db):
    """Get all contacts with count of linked clients, ordered by surname, name"""
    return db.execute("""
        SELECT c.id, c.name, c.surname, c.email,
        COUNT(cc.client_id) as client_count
        FROM contacts c
        LEFT JOIN client_contacts cc ON c.id = cc.contact_id
        GROUP BY c.id
        ORDER BY c.surname ASC, c.name ASC
    """).fetchall()

def get_contact_by_id(db, contact_id):
    """Get contact by ID"""
    return db.execute("""
        SELECT id, name, surname, email
        FROM contacts
        WHERE id = ?
    """, (contact_id,)).fetchone()

def get_linked_clients(db, contact_id):
    """Get all clients linked to a contact, ordered by client name"""
    return db.execute("""
        SELECT c.id, c.name, c.client_code
        FROM clients c
        INNER JOIN client_contacts cc ON c.id = cc.client_id
        WHERE cc.contact_id = ?
        ORDER BY c.name ASC
    """, (contact_id,)).fetchall()

def create_contact(db, name, surname, email):
    """Create a new contact"""
    cursor = db.execute(
        "INSERT INTO contacts (name, surname, email) VALUES (?, ?, ?)",
        (name, surname, email)
    )
    db.commit()
    return cursor.lastrowid

def update_contact(db, contact_id, name, surname, email):
    """Update an existing contact"""
    db.execute(
        "UPDATE contacts SET name = ?, surname = ?, email = ? WHERE id = ?",
        (name, surname, email, contact_id)
    )
    db.commit()

def link_contact_to_client(db, contact_id, client_id):
    """Link a contact to a client"""
    existing_link = db.execute(
        "SELECT client_id FROM client_contacts WHERE client_id = ? AND contact_id = ?",
        (client_id, contact_id)
    ).fetchone()
    
    if not existing_link:
        db.execute(
            "INSERT INTO client_contacts (client_id, contact_id) VALUES (?, ?)",
            (client_id, contact_id)
        )
        db.commit()

def unlink_contact_from_client(db, contact_id, client_id):
    """Unlink a contact from a client"""
    db.execute(
        "DELETE FROM client_contacts WHERE client_id = ? AND contact_id = ?",
        (client_id, contact_id)
    )
    db.commit()

def contact_email_exists(db, email, exclude_contact_id=None):
    """Check if email already exists (optionally excluding a specific contact)"""
    if exclude_contact_id:
        return db.execute(
            "SELECT id FROM contacts WHERE email = ? AND id != ?",
            (email, exclude_contact_id)
        ).fetchone() is not None
    else:
        return db.execute(
            "SELECT id FROM contacts WHERE email = ?",
            (email,)
        ).fetchone() is not None
