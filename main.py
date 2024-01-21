from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from data_b import db
from b_app import books_routes  
from c_app import customers_route
from loan_app import loans_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

CORS(app, origins="http://127.0.0.1:5500")
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

app.register_blueprint(books_routes)
app.register_blueprint(customers_route)
app.register_blueprint(loans_routes)

if __name__ == '__main__':
    app.run(debug=True)