"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add some users to seed the database with
leo = User(first_name='Leonardo', last_name='Turtle', image_url='https://cdn.shopify.com/s/files/1/0256/6537/2232/products/tmntleonardoenamelpin_700x495.png?v=1632458448')
donnie = User(first_name='Donatello', last_name='Turtle', image_url='https://cdn.shopify.com/s/files/1/0256/6537/2232/products/tmntdonatelloenamelpin_700x495.png?v=1632457950')
splinter = User(first_name='Master', last_name='Splinter', image_url='https://cdn.shopify.com/s/files/1/0411/2256/2201/products/NYCCC_PizzaRat-Sticker_proof_500x.webp?v=1673283651')

# Add new objects to session, so they'll persist
db.session.add(leo)
db.session.add(donnie)
db.session.add(splinter)

# Commit them to db
db.session.commit()
