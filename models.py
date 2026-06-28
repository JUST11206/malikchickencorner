# from database import db


# class User(db.Model):

#     id = db.Column(
#         db.Integer,
#         primary_key=True
#     )

#     fullname = db.Column(
#         db.String(100),
#         nullable=False
#     )

#     email = db.Column(
#         db.String(120),
#         unique=True,
#         nullable=False
#     )

#     phone = db.Column(
#         db.String(20),
#         nullable=False
#     )

#     password = db.Column(
#         db.String(200),
#         nullable=False
#     )


#     def __repr__(self):
#         return self.email
    
# models.py

from database import db
from datetime import datetime


# ==========================
# User Model
# ==========================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    phone = db.Column(db.String(20), unique=True)

    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    role = db.Column(
    db.String(20),
    default="customer",
    nullable=False
)

    def __repr__(self):
        return f"<User {self.fullname}>"
    
    # ==========================
# Product Model
# ==========================

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text)

    price = db.Column(db.Numeric(10,2), nullable=False)

    image = db.Column(db.String(255))

    stock = db.Column(db.Integer, default=0)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id")
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationship
    category = db.relationship(
        "Category",
        backref="products"
    )

    def __repr__(self):
        return f"<Product {self.name}>"
    


# ==========================
# Category Model
# ==========================

class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
    db.String(100),
    unique=True,
    nullable=False
)
    
    image = db.Column(db.String(255))


# ==========================
# Wishlist Model
# ==========================
class Wishlist(db.Model):

    __tablename__ = "wishlist"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    product = db.relationship("Product")

# ==========================
# Cart Model
# ==========================
class Cart(db.Model):

    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    

# ==========================
# Order Model
# ==========================
class Order(db.Model):

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    total_amount = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="orders"
    )
# ==========================
# Order Item Model
# ==========================

class OrderItem(db.Model):

    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    price = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

# ==========================
# Payment Model
# ==========================

class Payment(db.Model):

    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer,
                         db.ForeignKey("orders.id"))
    
    amount = db.Column(
    db.Numeric(10,2),
    nullable=False
)


    payment_method = db.Column(db.String(50))

    payment_status = db.Column(db.String(50))

    transaction_id = db.Column(db.String(255))

    created_at = db.Column(
    db.DateTime,
    default=datetime.utcnow
)


# ==========================
# Review Model
# ==========================

class Review(db.Model):

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))

    product_id = db.Column(db.Integer,
                           db.ForeignKey("products.id"))

    rating = db.Column(
    db.Integer,
    nullable=False
)

    comment = db.Column(db.Text)
