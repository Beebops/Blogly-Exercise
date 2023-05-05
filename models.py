from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone

db = SQLAlchemy()

DEFAULT_IMG_URL = 'https://img.freepik.com/premium-vector/avatar-profile-icon_188544-4755.jpg?w=1060'

def connect_db(app):
    """Connect this database to provided Flask app"""
    db.app = app
    db.init_app(app)

"""Models for Blogly."""
class User(db.Model):
    """A User has many Posts"""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                           nullable=False)
    
    last_name = db.Column(db.String(50),
                          nullable=True)
    
    image_url = db.Column(db.String(),
                          nullable=False,
                          default=DEFAULT_IMG_URL)
    
    posts = db.relationship('Post', backref='author', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __repr__(self):
        u = self
        return f"<User id:{u.id} first_name:{u.first_name} last_name:{u.last_name}"

class Post(db.Model):
    """Each Post has one User and each Post can have many Tags"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(75),
                      nullable=False)
    
    content = db.Column(db.Text(),
                        nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone('UTC')), nullable=False)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    #author = db.relationship('User')

    @property
    def show_date(self):
        """Return easy to read formatted date"""
        return self.created_at.strftime('%a %b %-d  %Y, %-I:%M %p')
    
    def __repr__(self):
        p = self
        created_at_formatted = p.created_at.astimezone(timezone('US/Eastern')).strftime('%A, %B %d, %Y %I:%M %p')

        return f'<Post id:{p.id} title: {p.title} created_at: {created_at_formatted} user_id {p.user_id}>'

class Tag(db.Model):
    """A Tag can be applied to many Posts"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True)
    
    name = db.Column(db.String, nullable=False, unique=True)

    posts = db.relationship('Post',
                            secondary='post_tags',
                            cascade='all, delete',
                            backref='tags')
    
    def __repr__(self):
        return f"<Tag id:{self.id} name: {self.name}"
    
class PostTag(db.Model):
    """Joins together a Post and a Tag"""
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)

    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True) 

    def __repr__(self):
        return f"<post_id:{self.post_id} tag_id: {self.tag_id}"  