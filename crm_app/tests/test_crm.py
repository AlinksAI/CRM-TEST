from crm_app.tests.base import BaseTestCase, db
from crm_app.models import Customer, User
from flask import url_for

class CRMTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        # Create another user for testing ownership
        self.other_user = User(username='otheruser', email='other@example.com')
        self.other_user.set_password('otherpass')
        db.session.add(self.other_user)
        db.session.commit()

    def test_customer_list_page_redirects_when_not_logged_in(self):
        with self.app.app_context():
            response = self.client.get(url_for('customer.list_customers'), follow_redirects=True)
        self.assertIn(b'Login', response.data) # Should be redirected to login
        self.assertIn(b'Please log in to access this page.', response.data)


    def test_customer_list_page_loads_when_logged_in(self):
        self.login_test_user()
        with self.app.app_context():
            response = self.client.get(url_for('customer.list_customers'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customers', response.data)
        self.logout_test_user()

    def test_add_customer(self):
        self.login_test_user()
        with self.app.app_context():
            response = self.client.post(url_for('customer.add_customer'), data=dict(
                first_name='John',
                last_name='Doe',
                email='john.doe@example.com',
                phone='1234567890',
                company='Doe Inc.',
                notes='Test customer'
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customer added successfully!', response.data)
        customer = Customer.query.filter_by(email='john.doe@example.com').first()
        self.assertIsNotNone(customer)
        self.assertEqual(customer.first_name, 'John')
        self.assertEqual(customer.user_id, self.test_user.id)
        self.logout_test_user()

    def test_edit_own_customer(self):
        self.login_test_user()
        # Add a customer first
        with self.app.app_context(): # Ensure app context for db operations and url_for
            customer = Customer(first_name='Jane', last_name='Doe', email='jane@example.com', user_id=self.test_user.id)
            db.session.add(customer)
            db.session.commit()

            response = self.client.post(url_for('customer.edit_customer', customer_id=customer.id), data=dict(
                first_name='Jane Updated',
                last_name='Doe Updated',
                email='jane.updated@example.com', # Required by form, even if not changing all fields
                phone=customer.phone,
                company=customer.company,
                notes=customer.notes
            ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customer updated successfully!', response.data)
        # Fetch from db within context if needed, or ensure session is active
        updated_customer = db.session.get(Customer, customer.id)
        self.assertEqual(updated_customer.first_name, 'Jane Updated')
        self.logout_test_user()

    def test_cannot_view_others_customer_detail(self):
        self.login_test_user() # Log in as test_user
        # Create a customer for other_user
        with self.app.app_context():
            other_customer = Customer(first_name='OtherView', last_name='Cust', email='otherview@example.com', user_id=self.other_user.id)
            db.session.add(other_customer)
            db.session.commit()
            # Try to view other_user's customer
            response = self.client.get(url_for('customer.view_customer', customer_id=other_customer.id))
        self.assertEqual(response.status_code, 403) # Forbidden
        self.logout_test_user()

    def test_cannot_edit_others_customer(self):
        self.login_test_user()
        with self.app.app_context():
            other_customer = Customer(first_name='OtherEdit', last_name='Cust', email='otheredit@example.com', user_id=self.other_user.id)
            db.session.add(other_customer)
            db.session.commit()

            response_get = self.client.get(url_for('customer.edit_customer', customer_id=other_customer.id))
            self.assertEqual(response_get.status_code, 403)

            response_post = self.client.post(url_for('customer.edit_customer', customer_id=other_customer.id), data=dict(
                first_name='Attempt Edit', last_name='Cust', email='otheredit@example.com' # required fields for form
            ), follow_redirects=True)
            self.assertEqual(response_post.status_code, 403)
        self.logout_test_user()

    def test_delete_own_customer(self):
        self.login_test_user()
        with self.app.app_context():
            customer = Customer(first_name='ToDelete', last_name='User', email='delete@example.com', user_id=self.test_user.id)
            db.session.add(customer)
            db.session.commit()
            customer_id = customer.id

            response = self.client.post(url_for('customer.delete_customer', customer_id=customer_id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Customer deleted successfully!', response.data)
        deleted_customer = db.session.get(Customer, customer_id) # Re-fetch after commit
        self.assertIsNone(deleted_customer)
        self.logout_test_user()

    def test_cannot_delete_others_customer(self):
        self.login_test_user()
        with self.app.app_context():
            other_customer = Customer(first_name='OtherDelete', last_name='Cust', email='otherdel@example.com', user_id=self.other_user.id)
            db.session.add(other_customer)
            db.session.commit()

            response = self.client.post(url_for('customer.delete_customer', customer_id=other_customer.id), follow_redirects=True)
        self.assertEqual(response.status_code, 403) # Forbidden
        self.assertIsNotNone(db.session.get(Customer, other_customer.id)) # Should still exist
        self.logout_test_user()
