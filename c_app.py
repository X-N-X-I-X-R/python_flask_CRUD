
from flask import jsonify, request
from flask import Blueprint
from models.customer_m import Customer
from data_b import db


customers_route = Blueprint('customers_route', __name__)

@customers_route.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])

@customers_route.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], years_old=data['years_old'], activated=data['activated'],)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(new_customer.to_dict()), 201

@customers_route.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer_id(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_dict())

@customers_route.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()

    # Update the customer object with the new data
    for key, value in data.items():
        setattr(customer, key, value)

    db.session.commit()
    return jsonify(customer.to_dict())

@customers_route.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204



