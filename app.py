import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'market.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(250))
    image = db.Column(db.String(250), default="https://via.placeholder.com/300x200")

    def __init__(self, name, price, description=None, image=None):
        self.name = name
        self.price = price
        self.description = description
        if image:
            self.image = image

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    cart_count = sum(session.get('cart', {}).values())
    return render_template('index.html', products=products, cart_count=cart_count)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    product_id_str = str(product_id)
    if product_id_str in session['cart']:
        session['cart'][product_id_str] += 1
    else:
        session['cart'][product_id_str] = 1
    
    session.modified = True
    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('index'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        action = request.form.get('action')
        
        if 'cart' in session and product_id in session['cart']:
            if action == 'increase':
                session['cart'][product_id] += 1
            elif action == 'decrease':
                session['cart'][product_id] -= 1
                if session['cart'][product_id] <= 0:
                    session['cart'].pop(product_id)
            elif action == 'remove':
                session['cart'].pop(product_id)
            session.modified = True
            return redirect(url_for('cart'))
        
    cart_items = []
    total = 0
    if 'cart' in session:
        for product_id, quantity in session['cart'].items():
            product = Product.query.get(int(product_id))
            if product:
                subtotal = product.price * quantity
                total += subtotal
                cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
    
    cart_count = sum(session.get('cart', {}).values())
    return render_template('cart.html', cart_items=cart_items, total=total, cart_count=cart_count)

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'cart' not in session or not session['cart']:
        flash('Seu carrinho está vazio.', 'error')
        return redirect(url_for('index'))
        
    cart_items = []
    total = 0
    for product_id, quantity in session['cart'].items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
            
    session.pop('cart', None)
    
    return render_template('checkout.html', cart_items=cart_items, total=total, cart_count=0)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
