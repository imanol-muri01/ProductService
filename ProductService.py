import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

#Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    #Product_id so we can search the product
    id = db.Column(db.Integer, primary_key=True)
    #Product Name
    name = db.Column(db.String(100), nullable=False)
    #The Price of the Product
    price = db.Column(db.REAL, nullable=False)
    #How many products are available
    quantity = db.Column(db.Integer, nullable=False)
    #If done or not. Relates to quantity.
    done = db.Column(db.Boolean, default=False)

# Endpoint 1: Get all products
@app.route('/products', methods=['GET'])
def get_products():
    #Get everything in the DB
    products = Product.query.all()
    #Put in a object
    product_list = [{"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity, "done" :product.done} for product in products]
    #Return a JSON
    return jsonify({"products": product_list})

# Endpoint 2: Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    #Query for anything with the product_id since id is our primary_key
    product = Product.query.get(product_id)
    #If product is not null the return JSON with object. Only returns on object.
    if product:
        return jsonify({"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity, "done" :product.done})
    #If product is null then it return a product not found error.
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint 3: Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    #Get information from the request payload. JSON format.
    data = request.json
    #In order to complete POST we should have a name, price, and quantity of products in our request.
    if ("name" not in data) or ("price" not in data) or ("quantity" not in data):
        #If not then we return a JSON of requirements to the server.
        return jsonify({"error": "Name/price/quantity is required"}), 400

    #If requirements are met then we make a product object.
    new_product = Product(name=data['name'], price=data['price'], quantity=data['quantity'], done=False)
    #Attach to the DB.
    db.session.add(new_product)
    db.session.commit()
    #Return a JSON with what was Made.
    return jsonify({"message": "Product created", "product": {"id": new_product.id, "name": new_product.name, "price": new_product.price, "quantity": new_product.quantity, "done" :new_product.done}}), 201

if __name__ == '__main__':
    #db.create_all()
    #Runs of port 5000, only useful for local host.
    app.run(debug=True,port=5000)
