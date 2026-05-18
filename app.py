import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session'

diretorio_atual = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(diretorio_atual, 'market.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(50), default='cliente', nullable=False) # 'admin' ou 'cliente'

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

with app.app_context():
    db.create_all()
    
    todas_pessoas = Usuario.query.all()
    admin_ja_existe = False
    for u in todas_pessoas:
        if u.email == 'admin@admin.com':
            admin_ja_existe = True
            
    if admin_ja_existe == False:
        admin_semente = Usuario(nome="Administrador", email="admin@admin.com", senha="vilsaoreidopython")
        admin_semente.cargo = "admin"
        db.session.add(admin_semente)
        db.session.commit()
        print("Conta admin semeada com sucesso!")

@app.route('/')
def index():
    print("Carregando a página inicial do site...")
    
    todos_produtos = Produto.query.all()
    
    maior_preco_do_banco = 0
    for p in todos_produtos:
        if p.preco > maior_preco_do_banco:
            maior_preco_do_banco = p.preco
            
    if maior_preco_do_banco == 0:
        maior_preco_do_banco = 10000
        
    pesquisa = request.args.get('q', '')
    if pesquisa != '':
        lista_filtrada = []
        for p in todos_produtos:
            nome_minusculo = p.nome.lower()
            desc_minuscula = p.descricao.lower()
            pesquisa_minuscula = pesquisa.lower()
            if pesquisa_minuscula in nome_minusculo or pesquisa_minuscula in desc_minuscula:
                lista_filtrada.append(p)
        todos_produtos = lista_filtrada
        
    # Filtro de preço mínimo na mão
    min_preco = request.args.get('min_preco', '')
    if min_preco != '':
        try:
            min_float = float(min_preco.replace(',', '.'))
            if min_float < 0:
                min_float = 0.0
                min_preco = '0.0'
            lista_filtrada = []
            for p in todos_produtos:
                if p.preco >= min_float:
                    lista_filtrada.append(p)
            todos_produtos = lista_filtrada
        except:
            print("Deu erro ao converter o preço mínimo!")
            
    # Filtro de preço máximo na mão
    max_preco = request.args.get('max_preco', '')
    if max_preco != '':
        try:
            max_float = float(max_preco.replace(',', '.'))
            if max_float < 0:
                max_float = 0.0
                max_preco = '0.0'
            lista_filtrada = []
            for p in todos_produtos:
                if p.preco <= max_float:
                    lista_filtrada.append(p)
            todos_produtos = lista_filtrada
        except:
            print("Deu erro ao converter o preço máximo!")
            
    total_itens = 0
    carrinho_dict = {}
    if 'cart' in session:
        carrinho_dict = session['cart']
        for chave in carrinho_dict:
            total_itens = total_itens + carrinho_dict[chave]
            
    print("Tudo certo! Renderizando os produtos na tela.")
    return render_template('index.html', products=todos_produtos, cart_count=total_itens, pesquisa=pesquisa, min_preco=min_preco, max_preco=max_preco, maior_preco=maior_preco_do_banco, carrinho=carrinho_dict)

# Rota de Cadastro de Usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    print("Alguém entrou na rota de cadastro!")
    
    if request.method == 'POST':
        nome_digitado = request.form['nome']
        email_digitado = request.form['email']
        senha_digitada = request.form['senha']
        
        if nome_digitado == '' or email_digitado == '' or senha_digitada == '':
            flash('Por favor, preencha todos os campos!', 'error')
            return redirect(url_for('cadastro'))
            
        todos_usuarios = Usuario.query.all()
        email_ja_existe = False
        for u in todos_usuarios:
            if u.email == email_digitado:
                email_ja_existe = True
                
        if email_ja_existe == True:
            flash('Este e-mail já está cadastrado!', 'error')
            return redirect(url_for('cadastro'))
            
        novo_u = Usuario(nome=nome_digitado, email=email_digitado, senha=senha_digitada)
        novo_u.cargo = "cliente"
        db.session.add(novo_u)
        db.session.commit()
        
        print("Usuário cadastrado com sucesso!")
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('cadastro.html', cart_count=0)

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Alguém entrou na rota de login!")
    
    if request.method == 'POST':
        email_digitado = request.form['email']
        senha_digitada = request.form['senha']
        
        # Procura no banco de dados com laço for
        todos_usuarios = Usuario.query.all()
        usuario_encontrado = None
        for u in todos_usuarios:
            if u.email == email_digitado:
                if u.senha == senha_digitada:
                    usuario_encontrado = u
                    
        if usuario_encontrado != None:
            session['usuario_id'] = usuario_encontrado.id
            session['usuario_nome'] = usuario_encontrado.nome
            session['usuario_cargo'] = usuario_encontrado.cargo
            print("Login deu certo!")
            flash('Login realizado com sucesso! Bem-vindo.', 'success')
            return redirect(url_for('index'))
        else:
            print("Email ou senha errada!")
            flash('E-mail ou senha incorretos!', 'error')
            return redirect(url_for('login'))
            
    return render_template('login.html', cart_count=0)

# Rota de Logout
@app.route('/logout')
def logout():
    print("Limpando a sessão do usuário...")
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    session.pop('usuario_cargo', None)
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('index'))

# Rota de Cadastro de Novos Produtos (só quem tá logado e é admin podeeee)
@app.route('/novo_produto', methods=['GET', 'POST'])
def novo_produto():
    print("Alguém quer cadastrar um produto novo...")
    
    if 'usuario_id' not in session:
        print("Ih! Não tá logado, não pode cadastrar.")
        flash('Você precisa estar logado para cadastrar um produto!', 'error')
        return redirect(url_for('login'))
        
    # Proteção por cargo
    if session.get('usuario_cargo') != 'admin':
        print("Tentativa de acesso não autorizada!")
        flash('Apenas administradores podem cadastrar produtos!', 'error')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        nome_p = request.form['nome']
        preco_p = request.form['preco']
        descricao_p = request.form['descricao']
        imagem_p = request.form['imagem']
        
        # O preço nunca pode ser negativo!!!!!!!!!!!!
        try:
            preco_float = float(preco_p.replace(',', '.'))
            if preco_float < 0:
                flash('O preço do produto não pode ser negativo!', 'error')
                return redirect(url_for('novo_produto'))
        except:
            flash('O preço precisa ser um número válido!', 'error')
            return redirect(url_for('novo_produto'))
            
        if nome_p == '' or preco_p == '':
            flash('Nome e Preço são obrigatórios!', 'error')
            return redirect(url_for('novo_produto'))
            
        if imagem_p == '':
            imagem_p = None
            
        novo_prod = Produto(nome=nome_p, preco=preco_float, descricao=descricao_p, imagem=imagem_p)
        db.session.add(novo_prod)
        db.session.commit()
        
        print("Produto cadastrado com sucesso no banco!")
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
        
    return render_template('novo_produto.html', cart_count=0)

@app.route('/add_to_cart/<int:id_do_produto>', methods=['POST'])
def add_to_cart(id_do_produto):
    print("Adicionando produto de id " + str(id_do_produto) + " ao carrinho...")
    
    if 'cart' not in session:
        session['cart'] = {}
        
    id_texto = str(id_do_produto)
    meu_carrinho = session['cart']
    
    # Se ja tem o produto no carrinho, soma 1
    ja_tem = False
    for item in meu_carrinho:
        if item == id_texto:
            meu_carrinho[item] = meu_carrinho[item] + 1
            ja_tem = True
            
    if ja_tem == False:
        meu_carrinho[id_texto] = 1
        
    session['cart'] = meu_carrinho
    session.modified = True
    print("Carrinho atualizado!")
    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('index'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    print("Alguém acessou a rota do carrinho!")
    
    if request.method == 'POST':
        id_prod_form = request.form.get('product_id')
        acao_form = request.form.get('action')
        proxima_pagina = request.form.get('proxima_pagina', 'cart')
        
        meu_carrinho = session['cart']
        
        if id_prod_form in meu_carrinho:
            if acao_form == 'increase':
                meu_carrinho[id_prod_form] = meu_carrinho[id_prod_form] + 1
                
            if acao_form == 'decrease':
                meu_carrinho[id_prod_form] = meu_carrinho[id_prod_form] - 1
                if meu_carrinho[id_prod_form] == 0:
                    del meu_carrinho[id_prod_form]
                    
            if acao_form == 'remove':
                del meu_carrinho[id_prod_form]
                
        session['cart'] = meu_carrinho
        session.modified = True
        print("Mudou a quantidade do produto " + str(id_prod_form) + " no carrinho.")
        return redirect(url_for(proxima_pagina))
        
    itens_tela = []
    dinheiro_total = 0
    numero_itens = 0
    
    if 'cart' in session:
        meu_carrinho = session['cart']
        for id_texto in meu_carrinho:
            quantidade = meu_carrinho[id_texto]
            numero_itens = numero_itens + quantidade
            
            todos_p = Produto.query.all()
            produto_banco = None
            for p in todos_p:
                if str(p.id) == id_texto:
                    produto_banco = p
                    
            if produto_banco != None:
                sub = produto_banco.preco * quantidade
                dinheiro_total = dinheiro_total + sub
                
                item_carrinho = {}
                item_carrinho['product'] = produto_banco
                item_carrinho['quantity'] = quantidade
                item_carrinho['subtotal'] = sub
                
                itens_tela.append(item_carrinho)
                
    return render_template('cart.html', cart_items=itens_tela, total=dinheiro_total, cart_count=numero_itens)

@app.route('/checkout', methods=['POST'])
def checkout():
    print("Finalizando a compra do usuário!")
    
    if 'cart' not in session:
        flash('Seu carrinho está vazio.', 'error')
        return redirect(url_for('index'))
        
    meu_carrinho = session['cart']
    if len(meu_carrinho) == 0:
        flash('Seu carrinho está vazio.', 'error')
        return redirect(url_for('index'))
        
    itens_tela = []
    dinheiro_total = 0
    
    for id_texto in meu_carrinho:
        quantidade = meu_carrinho[id_texto]
        
        # Procura no banco de dados na mão
        todos_p = Produto.query.all()
        produto_banco = None
        for p in todos_p:
            if str(p.id) == id_texto:
                produto_banco = p
                
        if produto_banco != None:
            sub = produto_banco.preco * quantidade
            dinheiro_total = dinheiro_total + sub
            
            item_carrinho = {}
            item_carrinho['product'] = produto_banco
            item_carrinho['quantity'] = quantidade
            item_carrinho['subtotal'] = sub
            
            itens_tela.append(item_carrinho)
            
    session['cart'] = {}
    session.modified = True
    
    print("Compra finalizada com sucesso! Limpando o carrinho.")
    return render_template('checkout.html', cart_items=itens_tela, total=dinheiro_total, cart_count=0)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
