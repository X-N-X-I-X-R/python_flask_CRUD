
from flask import jsonify, request
from flask import Blueprint
from models.customer_m import Customer
from data_b import db
from datetime import datetime, timedelta
from models.book_m import Book
from models.loan_m import Loan
from datetime import datetime



loans_routes = Blueprint('loans_routes', __name__)




@loans_routes.route('/loans', methods=['POST'])
def create_loan():
    data = request.get_json()
    
    # Validate that required fields are present in the request data
    if 'loanDate' not in data or 'bookID' not in data or 'customerID' not in data:
        return jsonify({'error': 'Required fields are missing in the request data (must be: loanDate, bookID, and customerID)'}, 400)
    
    loanDate_str = data['loanDate']
    bookID = data['bookID']
    customerID = data['customerID']
    
    # Validate the loanDate format
    try:
        loanDate = datetime.strptime(loanDate_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use the format YYYY-MM-DD'}), 400

    # Convert the loanDate string to a Python date object
    loanDate = datetime.strptime(loanDate_str, '%Y-%m-%d').date()

    # Check if the book with the specified bookID exists
    book = Book.query.get(bookID)

    # Check if the customer with the specified customerID exists
    customer = Customer.query.get(customerID)
    
    if book and book.status == 'available' and customer:
        # Update the book status to "unavailable"
        book.status = 'unavailable'

        # Create a new loan
        new_loan = Loan(loanDate=loanDate, bookID=bookID, customerID=customerID)
        db.session.add(new_loan)

        db.session.commit()

        return jsonify({'message': 'Loan created successfully!'})
    elif not customer:
        return jsonify({'error': 'Customer not found'}, 404)
    elif book and book.status == 'unavailable':
        return jsonify({'error': 'Book is already loaned'}, 400)
    else:
        return jsonify({'error': 'Book not found'}, 404)

# Route to retrieve all loans
@loans_routes.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    
    # Validation for when there are no activate loans
    if not loans:
        return jsonify({'error': 'There are no active loans'}), 404
    
    loan_list = [{'loanID': loan.loanID, 'loanDate': loan.loanDate, 'returnDate': loan.returnDate, 'bookID': loan.bookID, 'customerID': loan.customerID} for loan in loans]

    return jsonify({'loans': loan_list})

# Route to delete a loan by book id 
@loans_routes.route('/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if loan:
        # Update the book status to "available"
        book = Book.query.get(loan.bookID)
        book.status = 'available'

        db.session.delete(loan)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Loan not found'}, 404)
    

# Route to retrieve all loans by id 
@loans_routes.route('/loans/<int:loan_id>', methods=['GET'])
def get_loan_id(loan_id):
    loan = Loan.query.get(loan_id)
    if loan:
        return jsonify({'loanID': loan.loanID, 'loanDate': loan.loanDate, 'returnDate': loan.returnDate, 'bookID': loan.bookID, 'customerID': loan.customerID})
    else:
        return jsonify({'error': 'Loan not found'}, 404)



## Route to update a loan by loan id
@loans_routes.route('/loans/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    # Get the loan from the database
    loan = Loan.query.get(loan_id)

    # Check if the loan exists
    if loan:
        # Parse the data from the request
        data = request.get_json()

        # Update all fields if they are present in the request data
        for field in ['loanDate', 'bookID', 'customerID', 'returnDate']:
            if field in data:
                # Convert loanDate to a Python date object before updating
                if field == 'loanDate':
                    loanDate_str = data['loanDate']
                    try:
                        loanDate = datetime.strptime(loanDate_str, '%Y-%m-%d').date()
                    except ValueError:
                        return jsonify({'error': 'Invalid date format for loanDate. Please use the format YYYY-MM-DD'}), 400
                    setattr(loan, field, loanDate)
                elif field == 'returnDate':
                    returnDate_str = data['returnDate']
                    try:
                        returnDate = datetime.strptime(returnDate_str, '%Y-%m-%d').date()
                    except ValueError:
                        return jsonify({'error': 'Invalid date format for returnDate. Please use the format YYYY-MM-DD'}), 400
                    setattr(loan, field, returnDate)
                else:
                    setattr(loan, field, data[field])

        # Commit the changes to the database
        db.session.commit()

        return jsonify({'message': 'Loan updated successfully!'})
    else:
        return jsonify({'error': 'Loan not found'}, 404)
