from unittest import TestCase
import unittest
from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()



class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    def setUp(self):
        """Add sample user"""

        # Create all tables in the database
        db.create_all()

        # Create test fixtures
        User.query.delete()

        user = User(first_name='Zapp', last_name='Brannigan',
        image_url='https://static.wikia.nocookie.net/enfuturama/images/f/fe/Zapp_Brannigan_-_Official_Character_Promo.jpg/revision/latest?cb=20211008101815')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

       # Start a transaction
        self.connection = db.engine.connect()
        self.transaction = self.connection.begin() 

    def tearDown(self):
        """Roll back the transaction so that the database is left in its original state"""
        
        self.transaction.rollback()
        self.connection.close()

        # db.session.rollback()    

    def test_list_users(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Zapp', html)

    def test_add_new_user(self) :
         with app.test_client() as client:
             u = {'first_name': 'Phillip',
                  'last_name': 'Fry',
                  'image_url': 'https://upload.wikimedia.org/wikipedia/en/2/28/Philip_Fry.png'}   
             response = client.post('/users/new', data=d, follow_redirects=True)
             html = response.get_data(as_text=True) 

             self.assertEqual(response.status_code, 200)
             self.assertIn('<h2>Phillip Fry</h2>') 

if __name__ == '__main__':
    unittest.main()             