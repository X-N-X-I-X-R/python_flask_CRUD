from flask import jsonify, request
from flask import Blueprint
from models.book_m import Book
from data_b import db

books_routes = Blueprint('books_routes', __name__)

@books_routes.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@books_routes.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], year=data['year'], available=data['available'], loan_type=data['loan_type'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

@books_routes.route('/books/<int:book_id>', methods=['GET'])
def get_book_id(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict())
    



@books_routes.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    # Update the book object with the new data
    for key, value in data.items():
        setattr(book, key, value)

    db.session.commit()
    return jsonify(book.to_dict())

@books_routes.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

