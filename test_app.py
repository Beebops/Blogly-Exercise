from unittest import TestCase
import unittest
from app import app
from test_config import TestingConfig
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""

        # Create test fixtures
        User.query.delete()

        user = User(first_name='Zapp', last_name='Brannigan',
        image_url='https://static.wikia.nocookie.net/enfuturama/images/f/fe/Zapp_Brannigan_-_Official_Character_Promo.jpg/revision/latest?cb=20211008101815')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Roll back the transaction so that the database is left in its original state"""

        db.session.rollback()    

    def test_list_users(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Zapp', html)

if __name__ == '__main__':
    unittest.main()  
        