"""Seed file to make sample data for users db."""

from app import app
from models import User, Post, db

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add some users to seed the database
troy = User(first_name='Troy', last_name='McCLure', image_url='https://www.gannett-cdn.com/-mm-/02a053999b22cfd942b549e38f91ca1022b391ea/c=4-0-677-379/local/-/media/USATODAY/popcandy/2013/11/18//1384787123000-troy.jpg?width=660&height=372&fit=crop&format=pjpg&auto=webp')
zapp = User(first_name='Zapp', last_name='Brannigan', image_url='https://hips.hearstapps.com/esquire/assets/16/32/1471185929-zapp-brannigan.jpg')
farnsworth = User(first_name='Professor', last_name='Farnsworth', image_url='https://oyster.ignimgs.com/mediawiki/apis.ign.com/futurama/9/93/AntiPressure.jpg')
ned = User(first_name='Ned', last_name='Flanders', image_url='https://images.squarespace-cdn.com/content/v1/572a56b6b6aa60ae96b17dd3/1509766208684-0DIS9RGK7Z2SDSOSOVRT/Ned-flanders.jpg')
leela = User(first_name='Turanga', last_name='Leela', image_url='https://assets.mycast.io/actor_images/actor-turanga-leela-238366_large.jpg?1625486931')

# Add some posts to seed the database
p1 = Post(title='Good news, everyone!', content="Several years ago I tried to log on to AOL, and it just went through! Wheee! We're online!", author=farnsworth)
p2 = Post(title="Hi, I'm Troy Mcclure", content="You May Remember Me From Such Medical Films As Alice Doesn't Live Anymore And Mommy, What's Wrong With That Man's Face?", author=troy)
p3 = Post(title="Hi-dilly-ho, neighborinos!", content="I've done everything the Bible says — even the stuff that contradicts the other stuff!", author=ned)

# Add new objects to session, so they'll persist
db.session.add_all([troy, zapp, farnsworth, ned, leela, p1, p2, p3])

# Commit them to db
db.session.commit()
