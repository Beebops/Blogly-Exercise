"""Blogly application."""

from flask import Flask, request, render_template,  redirect
from models import db, connect_db, User
import os

def get_database_uri():
    if os.environ.get('flask-blogly') == 'Test':
        return 'postgresql:///blogly_test_db'
    return 'postgresql:///blogly'

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

#connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "mylittlesecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
app.debug = True

# db.create_all()
with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def redirect_to_users():
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('users/index.html', users=users)

@app.route('/users/new')
def new_user_form():
    """Shows form to add new user"""
    return render_template('users/new.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Adds a new user to db"""
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:user_id>/edit')
def user_edit_form(user_id):
    """Shows form to edit user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])    
def handle_edit_form(user_id):
    """Processes edit form and returns user to users page"""
    user=User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.img_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user from db"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')