CREATE TABLE clients (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT NOT NULL,
     client_code TEXT UNIQUE NOT NULL
);

CREATE TABLE contacts (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT NOT NULL,
     surname TEXT NOT NULL,
     email TEXT UNIQUE NOT NULL
);

CREATE TABLE client_contacts (
     client_id INTEGER,
     contact_id INTEGER,
     PRIMARY KEY(client_id,contact_id),
     FOREIGN KEY(client_id) REFERENCES clients(id),
     FOREIGN KEY(contact_id) REFERENCES contacts(id)
);

CREATE INDEX idx_client_name ON clients(name);
CREATE INDEX idx_contact_name ON contacts(surname,name);