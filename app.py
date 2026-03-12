from flask import Flask
from controllers.client_controller import client_routes
from controllers.contact_controller import contact_routes

app = Flask(__name__)

app.register_blueprint(client_routes)
app.register_blueprint(contact_routes)

if __name__ == "__main__":
    app.run(debug=True)