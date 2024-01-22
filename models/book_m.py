from data_b import db



class Book(db.Model):
    __tablename__ = 'books_updated'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True)
    loan_type = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='available')  # Add this line

    

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
