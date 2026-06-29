from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    session,
    url_for
    
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import Config
from database import db, init_db
from models import *
from models import Product
from werkzeug.utils import secure_filename
import os
from models import Cart, Product
from models import Wishlist
from sqlalchemy import func
from models import User, Order, Wishlist, Cart


app = Flask(__name__)

# Load configuration
app.config.from_object(Config)


# Initialize TiDB
init_db(app)


# Secret key
app.secret_key = app.config["SECRET_KEY"]


# ==========================
# Home
# ==========================
@app.route("/")
def home():
    return render_template("home/index.html")


# ==========================
# Menu
# ==========================
@app.route("/menu")
def menu():

    search = request.args.get("search", "")
    category = request.args.get("category", "")
    sort = request.args.get("sort", "")

    query = Product.query

    # Search
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # Category Filter
    if category:
        query = query.filter(Product.category_id == category)

    # Price Sorting
    if sort == "low":
        query = query.order_by(Product.price.asc())

    elif sort == "high":
        query = query.order_by(Product.price.desc())

    # Pagination
    page = request.args.get("page", 1, type=int)

    products = query.paginate(
        page=page,
        per_page=8,
        error_out=False
    )

    categories = Category.query.all()

    return render_template(
        "menu/menu.html",
        products=products,
        categories=categories
    )

# ==========================
# Authentication
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]


        user = User.query.filter_by(email=email).first()


        if user and check_password_hash(user.password, password):

            session["user_id"] = user.id
            session["fullname"] = user.fullname


            flash("Login successful!")

            return redirect(url_for("dashboard"))


        else:

            flash("Invalid email or password!")
            return redirect(url_for("login"))


    return render_template("auth/login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]


        # Check password match
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect("/signup")


        # Check existing email
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered!")
            return redirect("/signup")


        # Hash password
        hashed_password = generate_password_hash(password)


        user = User(
            fullname=fullname,
            email=email,
            phone=phone,
            password=hashed_password
        )


        db.session.add(user)
        db.session.commit()


        flash("Account created successfully!")
        return redirect("/login")


    return render_template("auth/signup.html")


@app.route("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_password.html")


#Dashboard user
# ==========================
# USER DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect("/login")

    user = db.session.get(User, session["user_id"])

    # Dashboard Statistics
    total_orders = Order.query.filter_by(
        user_id=user.id
    ).count()

    pending_orders = Order.query.filter_by(
        user_id=user.id,
        status="Pending"
    ).count()

    delivered_orders = Order.query.filter_by(
        user_id=user.id,
        status="Delivered"
    ).count()

    wishlist_count = Wishlist.query.filter_by(
        user_id=user.id
    ).count()

    cart_count = Cart.query.filter_by(
        user_id=user.id
    ).count()

    total_spent = db.session.query(
        db.func.sum(Order.total_amount)
    ).filter(
        Order.user_id == user.id
    ).scalar() or 0

    recent_orders = (
        Order.query
        .filter_by(user_id=user.id)
        .order_by(Order.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/dashboard.html",
        user=user,
        total_orders=total_orders,
        pending_orders=pending_orders,
        delivered_orders=delivered_orders,
        wishlist_count=wishlist_count,
        cart_count=cart_count,
        total_spent=total_spent,
        recent_orders=recent_orders
    )



@app.route("/admin/add-product", methods=["GET", "POST"])
def add_product():
    

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    categories = Category.query.all()

    if request.method == "POST":
        print(request.form)

        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        stock = request.form["stock"]
        category_id = request.form["category_id"]

        image = request.files["image"]

        filename = ""

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.static_folder,
                    "uploads/products",
                    filename
                )
            )

        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
            image="uploads/products/" + filename
        )

        db.session.add(product)
        db.session.commit()

        flash("Product Added Successfully!")

        return redirect(url_for("admin_dashboard"))

    return render_template(
        "admin/add_product.html",
        categories=categories
    )


# ==========================
# Manage Products
# ==========================
@app.route("/admin/manage-products")
def manage_products():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    products = Product.query.order_by(Product.id.desc()).all()

    return render_template(
        "admin/manage_products.html",
        products=products
    )

@app.route("/create-category")
def create_category():

    db.session.add(Category(name="Chicken"))
    db.session.add(Category(name="Fishes"))
    db.session.add(Category(name="Mutton"))
    db.session.add(Category(name="Drinks"))

    db.session.commit()

    return "Categories Created"

@app.route("/update-category")
def update_category():

    Category.query.filter_by(name="Burger").update(
        {"name": "Fishes"}
    )

    Category.query.filter_by(name="Pizza").update(
        {"name": "Mutton"}
    )

    db.session.commit()

    return "Updated Successfully"

#Edit Products
@app.route("/admin/edit-product/<int:id>", methods=["GET", "POST"])
def edit_product(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    product = Product.query.get_or_404(id)
    categories = Category.query.all()

    if request.method == "POST":

        product.name = request.form["name"]
        product.description = request.form["description"]
        product.price = request.form["price"]
        product.stock = request.form["stock"]
        product.category_id = request.form["category_id"]

        image = request.files["image"]

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.static_folder,
                    "uploads/products",
                    filename
                )
            )

            product.image = "uploads/products/" + filename

        db.session.commit()

        flash("Product Updated Successfully!")

        return redirect(url_for("manage_products"))

    return render_template(
        "admin/edit_product.html",
        product=product,
        categories=categories
    )

#Delete Products
@app.route("/admin/delete-product/<int:id>")
def delete_product(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    product = Product.query.get_or_404(id)

    # Delete Image
    if product.image:

        image_path = os.path.join(
            app.static_folder,
            product.image
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()

    flash("Product Deleted Successfully!")

    return redirect(url_for("manage_products"))

#product Detailed page route
@app.route("/product/<int:product_id>")
def product_detail(product_id):

    product = Product.query.get_or_404(product_id)

    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(4).all()

    return render_template(
        "menu/product_details.html",
        product=product,
        related_products=related_products
    )

#Search item
@app.route("/search")
def search():
    return "<h2>Search Feature Coming Soon</h2>"


# ==========================
# Cart
# ==========================


@app.route("/cart")
def cart():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cart_items = Cart.query.filter_by(
        user_id=user_id
    ).all()

    total = 0

    for item in cart_items:

        item.product = Product.query.get(item.product_id)

        total += float(item.product.price) * item.quantity

    return render_template(
        "cart/cart.html",
        cart_items=cart_items,
        total=total
    )



#cart-add
@app.route("/add-to-cart/<int:product_id>")
def add_to_cart(product_id):

    # Check Login
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Product already exists?
    cart_item = Cart.query.filter_by(
        user_id=user_id,
        product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity += 1

    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(cart_item)

    db.session.commit()

    return redirect("/cart")

#remove item 
@app.route("/remove-cart/<int:id>")
def remove_cart(id):

    item = Cart.query.get_or_404(id)

    db.session.delete(item)

    db.session.commit()

    return redirect("/cart")

#Increase Quantity
@app.route("/increase-cart/<int:id>")
def increase_cart(id):

    item = Cart.query.get_or_404(id)

    item.quantity += 1

    db.session.commit()

    return redirect("/cart")

#Decrease Quantity
@app.route("/decrease-cart/<int:id>")
def decrease_cart(id):

    item = Cart.query.get_or_404(id)

    if item.quantity > 1:
        item.quantity -= 1

    else:
        db.session.delete(item)

    db.session.commit()

    return redirect("/cart")


#Checkout Page

@app.route("/checkout")
def checkout():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cart_items = Cart.query.filter_by(user_id=user_id).all()

    for item in cart_items:
        item.product = Product.query.get(item.product_id)

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render_template(
        "checkout/checkout.html",
        cart_items=cart_items,
        total=total
    )

#Order Success route
@app.route("/order-success/<int:order_id>")
def order_success(order_id):

    if "user_id" not in session:
        return redirect("/login")

    order = Order.query.get_or_404(order_id)

    return render_template(
        "order/order_success.html",
        order=order
    )


# ==========================
# Wishlist
# ==========================

@app.route("/wishlist")
def wishlist():

    if "user_id" not in session:
        return redirect("/login")

    items = Wishlist.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "wishlist/wishlist.html",
        wishlist_items=items
    )


#Add wishlist

@app.route("/wishlist/add/<int:product_id>")
def add_to_wishlist(product_id):

    if "user_id" not in session:
        return redirect("/login")

    already = Wishlist.query.filter_by(
        user_id=session["user_id"],
        product_id=product_id
    ).first()

    if not already:

        item = Wishlist(
            user_id=session["user_id"],
            product_id=product_id
        )

        db.session.add(item)
        db.session.commit()

    return redirect(request.referrer or "/menu")

#Remove Wishlist
@app.route("/wishlist/remove/<int:id>")
def remove_wishlist(id):

    item = Wishlist.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    return redirect("/wishlist")


# ==========================
# My Order
# ==========================



@app.route("/my-orders")
def my_orders():

    if "user_id" not in session:
        return redirect("/login")

    orders = Order.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "orders/my_orders.html",
        orders=orders
    )

#Order Details Page 
@app.route("/order/<int:order_id>")
def order_details(order_id):

    if "user_id" not in session:
        return redirect("/login")

    order = Order.query.get_or_404(order_id)

    # Security check
    if order.user_id != session["user_id"]:
        flash("Unauthorized Access")
        return redirect("/my-orders")

    items = OrderItem.query.filter_by(
        order_id=order.id
    ).all()

    for item in items:
        item.product = Product.query.get(item.product_id)

        print("-----------")
        print("Product ID:", item.product_id)

        if item.product:
            print("Product Name:", item.product.name)
            print("Description:", item.product.description)
        else:
            print("Product Not Found")

    return render_template(
        "orders/order_details.html",
        order=order,
        items=items
    )
# ==========================
# Place Order
# ==========================

@app.route("/place-order" , methods =["POST"])
def place_order():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cart_items = Cart.query.filter_by(
        user_id=user_id
    ).all()

    if not cart_items:
        flash("Your cart is empty!")
        return redirect("/cart")

    total = 0

    for item in cart_items:

        product = Product.query.get(item.product_id)

        total += float(product.price) * item.quantity

    # Create Order
    order = Order(
        user_id=user_id,
        total_amount=total,
        status="Pending"
    )

    db.session.add(order)
    db.session.commit()

    # Save Order Items
    for item in cart_items:

        product = Product.query.get(item.product_id)

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )

        db.session.add(order_item)

    # Clear Cart
    Cart.query.filter_by(
        user_id=user_id
    ).delete()

    db.session.commit()

    return redirect(url_for("order_success", order_id=order.id))



# ==========================
# ADMIN ORDER 
# ==========================
#Admin Order Manage
@app.route("/admin/orders")
def admin_orders():

    if "admin_id" not in session:
        return redirect("/admin/login")

    orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "admin/manage_orders.html",
        orders=orders
    )

#Admin view order 
@app.route("/admin/order/<int:order_id>")
def admin_order_details(order_id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    order = Order.query.get_or_404(order_id)

    items = OrderItem.query.filter_by(
        order_id=order.id
    ).all()

    for item in items:
        item.product = db.session.get(Product, item.product_id)

    return render_template(
        "admin/admin_order_details.html",
        order=order,
        items=items
    )

#Status Change
@app.route("/admin/update-order/<int:order_id>/<status>")
def update_order(order_id, status):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    order = Order.query.get_or_404(order_id)

    allowed_status = [
        "Pending",
        "Confirmed",
        "Preparing",
        "Out For Delivery",
        "Delivered",
        "Cancelled"
    ]

    if status not in allowed_status:
        flash("Invalid Status")
        return redirect(url_for("admin_order_details", order_id=order.id))

    order.status = status

    db.session.commit()

    flash("Order Status Updated Successfully!")

    return redirect(url_for("admin_order_details", order_id=order.id))

#Status update 
@app.route("/admin/update-order/<int:order_id>/<status>")
def admin_update_order(order_id, status):

    if "admin_id" not in session:
        return redirect("/admin/login")

    order = Order.query.get_or_404(order_id)

    order.status = status

    db.session.commit()

    flash("Order Status Updated!")

    return redirect("/admin/orders")


# ==========================
# About
# ==========================
@app.route("/about")
def about():
    return render_template("about/about.html")

# ==========================
# Contact
# ==========================
@app.route("/contact")
def contact():
    return render_template("contact/contact.html")

# ==========================
# Gallery
# ==========================
@app.route("/gallery")
def gallery():
    return render_template("gallery/gallery.html")

# ==========================
# Offers
# ==========================
@app.route("/offers")
def offers():
    return render_template("offers/offers.html")

# ==========================
# Admin
# ==========================
# ==========================
# Admin Login
# ==========================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        admin = User.query.filter_by(
            email=email,
            role="admin"
        ).first()

        if admin and check_password_hash(admin.password, password):

            session["admin_id"] = admin.id
            session["admin_name"] = admin.fullname

            flash("Welcome Admin!")

            return redirect(url_for("admin_dashboard"))

        flash("Invalid Admin Credentials")

    return render_template("admin/login.html")


#Admin Dashboard
@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    total_products = Product.query.count()

    total_orders = Order.query.count()

    total_customers = User.query.filter_by(
        role="customer"
    ).count()

    pending_orders = Order.query.filter_by(
        status="Pending"
    ).count()

    revenue = db.session.query(
        db.func.sum(Order.total_amount)
    ).scalar() or 0

    recent_orders = Order.query.order_by(
        Order.created_at.desc()
    ).limit(5).all()
    print("Recent Orders Count:", len(recent_orders))

    # for order in recent_orders:
    #     print(
    #         "Order:", order.id,
    #         "User ID:", order.user_id,
    #         "User:", order.user
    # )
    return render_template(
        "admin/dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        total_customers=total_customers,
        pending_orders=pending_orders,
        revenue=revenue,
        recent_orders=recent_orders
    )


#Logout from Admin
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.context_processor
def inject_counts():

    cart_count = 0
    wishlist_count = 0

    if "user_id" in session:

        cart_count = Cart.query.filter_by(
            user_id=session["user_id"]
        ).count()

        wishlist_count = Wishlist.query.filter_by(
            user_id=session["user_id"]
        ).count()

    return dict(
        cart_count=cart_count,
        wishlist_count=wishlist_count
    )

# ==========================
# Run App
# ==========================
if __name__ == "__main__":
    app.run(debug=True)