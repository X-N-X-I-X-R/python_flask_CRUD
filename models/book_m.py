from data_b import db

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    loan_type = db.Column(db.Integer, nullable=False)
    
    # Establish a relationship with Review model
    reviews = db.relationship('Review', backref='book', cascade='all, delete-orphan', lazy=True)

    def __init__(self, title, author, year, available, loan_type):
        self.title = title
        self.author = author
        self.year = year
        self.available = available
        self.loan_type = loan_type
        
    def to_dict(self):    
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "available": self.available,
            "loan_type": self.loan_type
        }



