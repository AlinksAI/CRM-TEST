from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Customer, User # User might be needed for type hinting or complex queries
from ..forms import CustomerForm
from . import customer_bp

# Route: List Customers
@customer_bp.route('/')
@login_required
def list_customers():
    customers = Customer.query.filter_by(user_id=current_user.id).order_by(Customer.date_created.desc()).all()
    return render_template('customer/list_customers.html', customers=customers, title="Customers")

# Route: Add Customer
@customer_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            company=form.company.data,
            notes=form.notes.data,
            user_id=current_user.id
        )
        db.session.add(customer)
        db.session.commit()
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customer.list_customers'))
    return render_template('customer/add_edit_customer.html', form=form, title="Add New Customer")

# Route: View Customer
@customer_bp.route('/<int:customer_id>')
@login_required
def view_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.user_id != current_user.id:
        abort(403)  # Forbidden
    return render_template('customer/view_customer.html', customer=customer, title=f"{customer.first_name} {customer.last_name}")

# Route: Edit Customer
@customer_bp.route('/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.user_id != current_user.id:
        abort(403)

    form = CustomerForm(obj=customer) # Pre-populate form with customer data on GET

    if form.validate_on_submit(): # Process form data on POST
        form.populate_obj(customer) # Update customer object with form data
        db.session.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('customer.view_customer', customer_id=customer.id))

    return render_template('customer/add_edit_customer.html', form=form, title="Edit Customer", customer=customer)

# Route: Delete Customer
@customer_bp.route('/<int:customer_id>/delete', methods=['POST'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.user_id != current_user.id:
        abort(403)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('customer.list_customers'))
