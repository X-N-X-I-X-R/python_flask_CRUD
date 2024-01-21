from data_b import db

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    years_old = db.Column(db.Integer, nullable=False)
    activated = db.Column(db.Boolean, default=True)

    def __init__(self, name, email, years_old, activated):
        self.name = name
        self.email = email
        self.years_old = years_old
        self.activated = activated


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "years_old": self.years_old,
            "activated": self.activated,

        }