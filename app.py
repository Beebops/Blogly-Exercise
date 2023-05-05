"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash
from models import db, connect_db, User, Post, Tag
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///blogly'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "mylittlesecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
app.app_context().push()

@app.route('/')
def redirect_to_users():
    return redirect('/users')

# ------ User Views ------

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
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url', None)

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} added.")
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    full_name = user.full_name
    posts = user.posts

    return render_template('users/show.html', user=user, full_name=full_name, posts=posts)

@app.route('/users/<int:user_id>/edit')
def user_edit_form(user_id):
    """Shows form to edit user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])    
def handle_user_edit_form(user_id):
    """Processes edit form and returns user to users page"""
    user = User.query.get_or_404(user_id)
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    if user.first_name != first_name:
        user.first_name = first_name
    
    if user.last_name != last_name:
        user.last_name = last_name

    if user.image_url != image_url:
        user.image_url = image_url

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

 # ------ POSTS VIEWS ------

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Shows form to add a new post for a user"""
    user = User.query.get_or_404(user_id)
    full_name = user.full_name
    tags = Tag.query.all()
    return render_template('users/posts/new.html', user=user,tags=tags, full_name=full_name)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    """ Create a new Post and save to db"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(
       title = request.form['title'],
       content = request.form['content'],
       user_id = user_id,
       tags=tags)
    
    db.session.add(new_post)
    db.session.commit()
    flash(f'Post "{new_post}" added.')
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Shows a single post"""
    post = Post.query.get_or_404(post_id)
    
    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def post_edit_form(post_id):
    """Shows form to edit post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('/posts/edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete existing post from db"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    #flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")

# ------ TAG VIEWS ------
@app.route('/tags')
def tags_home():
    """Show info of all tags on the page"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)

@app.route('/tags/new')
def new_tag_form():
    """Shows form to create a new tag"""

    posts = Post.query.all()
    return render_template('/tags/new.html', posts=posts)

@app.route('/tags/new', methods=['POST'])
def new_tag():
    """Handle form to create a new tag"""
    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag {new_tag.name} has been added")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Shows the selected tag and a list of posts that are tagged with it"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/show.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """Shows form to edit a tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('/tags/edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """Handle form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlists('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Handle form to delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag {tag.name} has been deleted")
    return redirect('/tags')