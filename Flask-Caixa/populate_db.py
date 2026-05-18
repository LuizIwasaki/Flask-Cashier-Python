from app import app, db, Produto

def popular_banco():
    with app.app_context():
        quantidade_produtos = Produto.query.count()
        
        if quantidade_produtos == 0:
            meus_produtos = [
                Produto(nome="Smartphone XYZ", preco=2999.99, descricao="Última geração com câmera espetacular e bateria de longa duração.", imagem="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=600&auto=format&fit=crop"),
                Produto(nome="Notebook Pro", preco=7499.00, descricao="Potência extrema para profissionais e gamers com tela 4K.", imagem="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=600&auto=format&fit=crop"),
                Produto(nome="Fone Bluetooth", preco=399.50, descricao="Som cristalino com cancelamento de ruído ativo.", imagem="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=600&auto=format&fit=crop"),
                Produto(nome="Smartwatch Ultra", preco=1299.90, descricao="Monitore sua saúde e atividades com estilo inigualável.", imagem="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=600&auto=format&fit=crop"),
                Produto(nome="Câmera Mirrorless", preco=4500.00, descricao="Capture momentos perfeitos com lente intercambiável 50mm.", imagem="https://images.unsplash.com/photo-1516035069371-29a1b244cc32?q=80&w=600&auto=format&fit=crop"),
                Produto(nome="Teclado Mecânico", preco=450.00, descricao="Digitação precisa com switches mecânicos e RGB personalizável.", imagem="https://images.unsplash.com/photo-1595225476474-87563907a212?q=80&w=600&auto=format&fit=crop")
            ]
            
            for p in meus_produtos:
                db.session.add(p)
                
            db.session.commit()
            print("Banco de dados preenchido com sucesso!")
        else:
            print("O banco de dados já tem produtos.")

if __name__ == '__main__':
    popular_banco()
