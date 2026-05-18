import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'

# Configuração do banco de dados
diretorio_atual = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(diretorio_atual, 'market.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(250))
    imagem = db.Column(db.String(250), default="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=600&auto=format&fit=crop")

    def __init__(self, nome, preco, descricao=None, imagem=None):
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        if imagem:
            self.imagem = imagem

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Pega todos os produtos
    lista_produtos = Produto.query.all()
    
    # Conta quantos itens tem no carrinho
    total_itens = 0
    if 'cart' in session:
        for chave in session['cart']:
            total_itens = total_itens + session['cart'][chave]
            
    return render_template('index.html', products=lista_produtos, cart_count=total_itens)

# Adiciona produto ao carrinho
@app.route('/add_to_cart/<int:id_do_produto>', methods=['POST'])
def add_to_cart(id_do_produto):
    if 'cart' not in session:
        session['cart'] = {}
    
    id_texto = str(id_do_produto)
    meu_carrinho = session['cart']
    
    existe = False
    for item in meu_carrinho:
        if item == id_texto:
            meu_carrinho[item] = meu_carrinho[item] + 1
            existe = True
            
    if existe == False:
        meu_carrinho[id_texto] = 1
    
    session['cart'] = meu_carrinho
    session.modified = True
    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('index'))

# Carrinho de compras
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        id_do_produto = request.form.get('product_id')
        acao = request.form.get('action')
        meu_carrinho = session['cart']
        
        if id_do_produto in meu_carrinho:
            if acao == 'increase':
                meu_carrinho[id_do_produto] = meu_carrinho[id_do_produto] + 1
            
            if acao == 'decrease':
                meu_carrinho[id_do_produto] = meu_carrinho[id_do_produto] - 1
                if meu_carrinho[id_do_produto] == 0:
                    del meu_carrinho[id_do_produto]
            
            if acao == 'remove':
                del meu_carrinho[id_do_produto]
                
        session['cart'] = meu_carrinho
        session.modified = True
        return redirect(url_for('cart'))
        
    itens_do_carrinho = []
    valor_total = 0
    total_itens = 0
    
    if 'cart' in session:
        meu_carrinho = session['cart']
        for id_do_produto in meu_carrinho:
            quantidade = meu_carrinho[id_do_produto]
            total_itens = total_itens + quantidade
            
            todos_produtos = Produto.query.all()
            produto_encontrado = None
            for p in todos_produtos:
                if str(p.id) == id_do_produto:
                    produto_encontrado = p
            
            if produto_encontrado != None:
                subtotal = produto_encontrado.preco * quantidade
                valor_total = valor_total + subtotal
                
                item_atual = {}
                item_atual['product'] = produto_encontrado
                item_atual['quantity'] = quantidade
                item_atual['subtotal'] = subtotal
                
                itens_do_carrinho.append(item_atual)
    
    return render_template('cart.html', cart_items=itens_do_carrinho, total=valor_total, cart_count=total_itens)


# Checkout
@app.route('/checkout', methods=['POST'])
def checkout():
    if 'cart' not in session:
        flash('Seu carrinho está vazio.', 'error')
        return redirect(url_for('index'))
        
    meu_carrinho = session['cart']
    if len(meu_carrinho) == 0:
        flash('Seu carrinho está vazio.', 'error')
        return redirect(url_for('index'))
        
    itens_do_carrinho = []
    valor_total = 0
    
    for id_do_produto in meu_carrinho:
        quantidade = meu_carrinho[id_do_produto]
        
        todos_produtos = Produto.query.all()
        produto_encontrado = None
        for p in todos_produtos:
            if str(p.id) == id_do_produto:
                produto_encontrado = p
                
        if produto_encontrado != None:
            subtotal = produto_encontrado.preco * quantidade
            valor_total = valor_total + subtotal
            
            item_atual = {}
            item_atual['product'] = produto_encontrado
            item_atual['quantity'] = quantidade
            item_atual['subtotal'] = subtotal
            
            itens_do_carrinho.append(item_atual)
            
    # Limpa o carrinho
    session['cart'] = {}
    session.modified = True
    
    return render_template('checkout.html', cart_items=itens_do_carrinho, total=valor_total, cart_count=0)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
