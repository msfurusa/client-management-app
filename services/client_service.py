def generate_client_code(name, db):
    """
    Generate a unique 6-character client code in format AAA001
    - For multi-word names: first letter of each word
    - For single-word names: first 3 letters of the word
    - If result < 3 chars, pad with 'A's
    - Last 3 characters: numeric starting from 001, incremented until unique
    """
    # Split name into words
    words = name.split()

    if len(words) > 1:
        # Multi-word name: take first letter of each word
        prefix = ''.join(word[0] for word in words[:3]).upper()
    else:
        # Single-word name: take first 3 letters
        prefix = name[:3].upper()

    # Pad with 'A' if we have fewer than 3 characters
    prefix = prefix.ljust(3, 'A')

    # Start with 001 and increment until we find a unique code
    number = 1
    while True:
        code = f"{prefix}{number:03d}"

        # Check if this code already exists
        exists = db.execute(
            "SELECT id FROM clients WHERE client_code=?",
            (code,)
        ).fetchone()

        if not exists:
            return code

        number += 1