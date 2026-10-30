# NexStore | The Store of the Future 🚀

A modern, visually stunning, and responsive e-commerce web application built with **Python + Flask**, **Vanilla CSS (no Tailwind/Bootstrap)**, and an **SQLite** database.

This project combines an extremely premium and modern visual design (*Glassmorphism*, *Outfit* Google Font, smooth transitions, and Phosphor Icons library) with a simplified, didactical, and beginner-friendly backend codebase to make studying and quick testing seamless.

---

## 🌟 Key Features

1. **Product Catalog:** Elegant product cards loaded with high-quality imagery.
2. **Dynamic Cart Controls on Home:** Add items, increase or decrease quantities (`[ - ]  Qty  [ + ]`) directly on the product card inside the page, without page reloads!
3. **Search & Advanced Price Filter:**
   * Textual search in real-time.
   * Collapsible, minimalist price panel with smooth transition animations.
   * Numeric inputs with **real-time currency masking** (e.g., typing `8` formats to `0,08`, `1234` formats to `12,34`).
   * An interactive *Range Slider* synced in real-time with manual input fields.
4. **Authentication System (Login/Signup):**
   * Single unified and dynamic login button in the navbar.
   * Secure session control.
5. **Access Control (Admin vs Customer roles):**
   * **Customer:** Can browse products, filter prices, and add items to cart.
   * **Admin:** Admins have exclusive access to register new products (equipped with validation checks against negative prices).
   * The "New Product" menu button only displays in the navbar when logged in as an administrator.

---

## 🔑 Pre-seeded Admin Credentials

The database is initialized automatically with a default administrator account for testing:

* **Email:** `admin@admin.com`
* **Password:** `vilsaoreidopython`
* **Role:** `admin`

*Tip: You can log out from the admin account and sign up for a new standard user account to test the difference in permissions!*

---

## 🛠️ Install & Exec

Follow these simple steps to run the application locally:

### 1. Set up dependencies
Open the project folder in your terminal and install the required packages:
```bash
pip install -r requirements.txt
```

### 2. Populate the database (First run)
Run the populator script to create the SQLite database and seed initial products and admin:
```bash
python3 populate_db.py
```
*(This creates the `market.db` file in the root directory).*

### 3. Start the Flask server
Start the Python application:
```bash
python3 app.py
```

### 4. Open in Browser
Navigate to the following URL in your web browser:
```
http://localhost:5000
```

---

## 📁 Directory Structure

* `app.py`: The heart of the application. Contains all routes (Home, Login, Signup, Cart, Add Product), security constraints, database tables, and seeded credentials. Heavily commented in a student-friendly layout with debugging terminal logs.
* `populate_db.py`: A simple utility to fill the SQLite database with default products if empty.
* `requirements.txt`: Standard list containing only the essential packages (Flask and Flask-SQLAlchemy).
* `static/style.css`: Premium application styles (responsiveness, glassmorphism, sliders, custom masks).
* `templates/`: HTML structures dynamically rendered via the Jinja2 engine.
  * `base.html`: Common layout with interactive navbar, flash warning alerts, and session handlers.
  * `index.html`: Main marketplace page showing the collapsible filter panel and product cards.
  * `login.html` & `cadastro.html`: Semi-transparent authentication forms.
  * `novo_produto.html`: Safe product registration panel featuring real-time monetary input masks.
