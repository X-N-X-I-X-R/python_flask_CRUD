
from flask import jsonify, request
from flask import Blueprint
from models.customer_m import Customer
from data_b import db
from datetime import datetime
from models.book_m import Book
from models.loan_m import Loan
from sqlalchemy import func


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

# Route to end a loan by book title
@loans_routes.route('/loans', methods=['DELETE'])
def end_loan():

    book_title = request.args.get('q')
    if book_title:

        # Check if there is a book with a title that matches (case-insensitive)
        book = Book.query.filter(func.lower(Book.title) == func.lower(book_title)).first()

        if book:
            # Check if there is a loan for this book
            loan = Loan.query.filter_by(bookID=book.bookID).first()

            if loan:
                
                book.status = 'available'
                db.session.delete(loan)
                db.session.commit()

                return jsonify({'message': 'Loan ended successfully'})
            else:
                return jsonify({'error': 'No loan found for this book'}, 400)
        else:
            return jsonify({'error': 'Book not found'}, 404)
    else:
        return jsonify({'error': 'search quary is missing (parameter: q)'})

# Route to retrieve all late loans
@loans_routes.route('/loans/late', methods=['GET'])
def get_late_loans():
    current_date = datetime.now().date()

    late_loans = Loan.query.filter(Loan.returnDate < current_date).all()

    late_loan_list = [{'loanID': loan.loanID, 'loanDate': loan.loanDate, 'returnDate': loan.returnDate, 'bookID': loan.bookID, 'customerID': loan.customerID} for loan in late_loans]

    return jsonify({'late_loans': late_loan_list})


@loans_routes.route('/loans/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    try:
        loan = Loan.query.get(loan_id)
        if loan:
            data = request.get_json()
            # Update the loan attributes based on the data received
            loan.loanDate = datetime.strptime(data['loanDate'], '%Y-%m-%d').date()
            # Update other attributes as needed

            db.session.commit()
            return jsonify({'message': 'Loan updated successfully'})
        else:
            return jsonify({'error': 'Loan not found'}, 404)
    except Exception as e:
        return jsonify({'error': f'Error updating loan: {str(e)}'}), 500
