from unittest import TestCase
import os
from sqlalchemy import exc

os.environ['DATABASE_URL'] = 'postgresql:///blogly_test_db'

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.create_all()

class UserTestCase(TestCase):
	"""Tests for users"""

	def setUp(self):
		"""Create test user, add sample data"""
		
		db.drop_all()
		db.create_all()
		User.query.delete()
		
		user = User(first_name='Phillip', last_name='Fry', image_url='www.planetexpress.com')
		db.session.add(user)
		db.session.flush()

		self.user_id = user.id

	def tearDown(self):
		db.session.rollback()	
    
	def test_list_users(self):
		with app.test_client() as client:
			resp = client.get('/', follow_redirects=True)
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn('Fry', html)
    
	def test_add_new_user(self):
		with app.test_client() as client:
			client.post('/users/new',
		      data={'first_name': 'Professor', 'last_name': 'Farnsworth', 'image_url': 'www.futurama.com'})
			
			user = User.query.filter_by(last_name='Farnsworth').first()

			self.assertEqual(user.first_name, 'Professor')
			self.assertEqual(user.last_name, 'Farnsworth')

	def test_show_user_details(self):
		with app.test_client() as client:
			resp = client.get(f'/users/{self.user_id}')
			html = resp.get_data(as_text=True)

			self.assertEqual(resp.status_code, 200)
			self.assertIn('Farnsworth', html)
			self.assertIn('www.futurama.com', html)	

	def test_delete_user(self):
		with app.test_client() as client:
			resp = client.post(f'/users/{self.user_id}/delete')
			user = User.query.get(self.user_id)

			self.assertFalse(user)

	def test_handle_edit_form(self):
		with app.test_client() as client:
			resp = client.post(f'/users/{self.user_id}/edit',
		      data={'first_name': 'Amy', 'last_name': 'Wong', 'image_url': 'www.futurama.com'})
			
			user = User.query.get(self.user_id)
			self.assertEqual(user.first_name, 'Amy')
			self.assertEqual(user.last_name, 'Wong')
			self.assertEqual(user.image_url, 'www.futurama.com')
