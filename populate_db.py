from app import app, db, Product

def populate():
    with app.app_context():
        if Product.query.count() == 0:
            products = [
                Product(name="Smartphone XYZ", price=2999.99, description="Última geração com câmera espetacular e bateria de longa duração.", image="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=600&auto=format&fit=crop"),
                Product(name="Notebook Pro", price=7499.00, description="Potência extrema para profissionais e gamers com tela 4K.", image="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=600&auto=format&fit=crop"),
                Product(name="Fone Bluetooth", price=399.50, description="Som cristalino com cancelamento de ruído ativo.", image="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=600&auto=format&fit=crop"),
                Product(name="Smartwatch Ultra", price=1299.90, description="Monitore sua saúde e atividades com estilo inigualável.", image="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=600&auto=format&fit=crop"),
                Product(name="Câmera Mirrorless", price=4500.00, description="Capture momentos perfeitos com lente intercambiável 50mm.", image="https://images.unsplash.com/photo-1516035069371-29a1b244cc32?q=80&w=600&auto=format&fit=crop"),
                Product(name="Teclado Mecânico", price=450.00, description="Digitação precisa com switches mecânicos e RGB personalizável.", image="https://images.unsplash.com/photo-1595225476474-87563907a212?q=80&w=600&auto=format&fit=crop")
            ]
            db.session.add_all(products)
            db.session.commit()
            print("Database populated with sample products.")
        else:
            print("Database already populated.")

if __name__ == '__main__':
    populate()
