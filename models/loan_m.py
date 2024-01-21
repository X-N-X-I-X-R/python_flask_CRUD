from datetime import timedelta

from sqlalchemy import ForeignKeyConstraint
from models.book_m import Book
from data_b import db
class Loan(db.Model):
    __tablename__ = 'loans'

    loanID = db.Column(db.Integer, primary_key=True)
    loanDate = db.Column(db.Date, nullable=False)
    bookID = db.Column(db.Integer, db.ForeignKey('books_updated.id'), nullable=False)   
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    returnDate = db.Column(db.Date, nullable=False)

    # Data Integrity: Define a ForeignKeyConstraint to enforce the relationship
    __table_args__ = (
    ForeignKeyConstraint(['bookID'], ['books_updated.id']),
    ForeignKeyConstraint(['customerID'], ['customers.id']),
)

    def __init__(self, loanDate, bookID, customerID):
        self.loanDate = loanDate
        self.bookID = bookID
        self.customerID = customerID
        
        # Set the 'returnDate' based on the book's type
        book = Book.query.get(bookID)
        if book:
            if book.loan_type == 1:
                self.returnDate = loanDate + timedelta(days=10)
            elif book.loan_type == 2:
                self.returnDate = loanDate + timedelta(days=5)
            elif book.loan_type == 3:
                self.returnDate = loanDate + timedelta(days=2)