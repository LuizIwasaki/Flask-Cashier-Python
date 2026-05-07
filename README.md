# NexStore - Flask E-commerce

A modern, visually stunning, and responsive e-commerce web application built with Python, Flask, and Vanilla CSS. It simulates a complete marketplace checkout experience with sessions and an SQLite database.

## Features
- **Product Listing:** Browse available electronics with rich image cards.
- **Dynamic Cart System:** Add, remove, or adjust quantities of items in your cart (powered by Flask sessions).
- **Checkout Simulation:** Get a clear overview of your order and total price.
- **Premium UI/UX:** Built with high-quality Vanilla CSS, featuring glassmorphism, responsive grids, micro-animations, and the modern Outfit font.
- **Database Integrated:** Uses Flask-SQLAlchemy with an SQLite database to store product data.

## Technologies Used
- Python 3
- Flask
- Flask-SQLAlchemy (SQLite)
- HTML5 / Jinja2 Templates
- Vanilla CSS (No Bootstrap/Tailwind)
- Phosphor Icons

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Flask-Cashier-Python
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Populate the database:**
   Run the following script to generate the database and seed it with initial products.
   ```bash
   python3 populate_db.py
   ```

4. **Run the server:**
   ```bash
   python3 app.py
   ```

5. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`.

## Design Philosophy
This project was built focusing on "Visual Excellence". No generic UI frameworks were used. The design utilizes CSS Custom Properties, smooth transitions, box-shadows for depth, and carefully selected typography to create a premium, real-world e-commerce feel.