# database.py

from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy object
db = SQLAlchemy()


def init_db(app):
    """
    Initialize database with Flask app
    """
    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("✅ Database Connected Successfully!")