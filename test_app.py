from unittest import TestCase
import unittest
from app import app
#from test_config import TestingConfig
from models import db, User
import os

os.environ['flask-blogly'] = 'Test'

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
  db.drop_all()
  db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""
        os.environ['flask-blogly'] = 'Test'
        # Create test fixtures
        with app.app_context():
          User.query.delete()

          user = User(first_name='TestUserFirstName', last_name='TestUserLastName')
          db.session.add(user)
          db.session.commit()

          self.user_id = user.id

    def tearDown(self):
        """Roll back the transaction so that the database is left in its original state"""
        with app.app_context():
          db.session.rollback()

          os.environ.pop('flask-blogly')    

    def test_list_users(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('TestUserFirstName', html)

    def test_user_edit_form(self):
      with app.test_client() as client:
        #  with app.app_context():
        #   User.query.delete()

        #   user = User(first_name='TestUserFirstName', last_name='TestUserLastName')
        #   db.session.add(user)
        #   db.session.commit()

        #   self.user_id = user.id

         response = client.get(f'/users/{user.id}/edit')
         html = response.get_data(as_text=True)

         self.assertEqual(response.status_code, 200)
         self.assertIn('TestUserFirstName', html)    

if __name__ == '__main__':
    unittest.main()  
        