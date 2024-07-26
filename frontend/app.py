from flask import Flask, render_template, jsonify

app = Flask(__name__)

menu_data = [
    {"id": 1, "name": "Margherita Pizza", "price": 10.99,
     "description": "Classic Italian pizza with tomato sauce, mozzarella, and basil.", "image": "Margherita.jpg"},
    {"id": 2, "name": "Pepperoni Pizza", "price": 12.99,
     "description": "Delicious pizza topped with pepperoni slices and mozzarella cheese.", "image": "pepperoni.jpg"},
    {"id": 3, "name": "Vegetarian Pizza", "price": 11.99,
     "description": "Loaded with fresh vegetables like bell peppers, onions, mushrooms, and olives.",
     "image": "vegetarian.jpg"},
    {"id": 4, "name": "Hawaiian Pizza", "price": 13.99,
     "description": "A tropical delight with ham, pineapple, and mozzarella cheese.", "image": "hawaiian.jpg"},
    {"id": 5, "name": "BBQ Chicken Pizza", "price": 14.99,
     "description": "Tender chicken, tangy BBQ sauce, red onions, and cilantro atop our signature crust.",
     "image": "bbq_chicken.jpg"},
    {"id": 6, "name": "Supreme Pizza", "price": 15.99,
     "description": "The ultimate pizza loaded with pepperoni, sausage, bell peppers, onions, and mushrooms.",
     "image": "supreme.jpg"},
    {"id": 7, "name": "Four Cheese Pizza", "price": 9.99, "description": "Simple yet satisfying classic cheese pizza.",
     "image": "Four cheese.jpg"},
    {"id": 8, "name": "Mushroom Pizza", "price": 11.99,
     "description": "Delicious pizza loaded with fresh mushrooms and mozzarella cheese.", "image": "mushroom_pizza.jpg"}
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
def show_menu():
    return render_template('menu.html', menu=menu_data)


@app.route('/menu/data')
def get_menu():
    return jsonify(menu_data), 200


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/special_offers')
def special_offers():
    return render_template('special_offers.html')


@app.route('/view_cart')
def view_cart():
    return render_template('cart.html')


@app.route('/auth/signup')
def register_page():
    return render_template('register.html')


@app.route('/auth/login')
def login_page():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
