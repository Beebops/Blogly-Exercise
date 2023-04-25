from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = 'https://img.freepik.com/premium-vector/avatar-profile-icon_188544-4755.jpg?w=1060'

def connect_db(app):
    """Connect this database to provided Flask app"""
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                           nullable=False)
    
    last_name = db.Column(db.String(50),
                          nullable=False)
    
    image_url = db.Column(db.String(),
                          nullable=False,
                          default=DEFAULT_IMG_URL)
    
    def __repr__(self):
        u = self
        return f"<User id:{u.id} first_name:{u.first_name} last_name:{u.last_name}"