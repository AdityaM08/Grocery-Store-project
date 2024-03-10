from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import date, datetime

DB = SQLAlchemy()

class User(DB.Model):
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String, nullable=False, unique=True)
    user_name = Column(String, nullable=False)
    user_password = Column(String, nullable=False)
    role = Column(String(), default='user', nullable=False)
    latest_log = Column(String(), default = datetime.utcnow (), nullable=False)

    products = relationship('Product', secondary='cart', back_populates='users')
    orders = relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f"User({self.email}, {self.username}, {self.role})"

class Manager(DB.Model):
    manager_id = Column(Integer, primary_key=True, autoincrement=True)
    manager_email = Column(String, nullable=False, unique=True)
    manager_name = Column(String, nullable=False)
    manager_password = Column(String, nullable=False)
    manager_status = Column(String(), default="Pending", nullable=False)

    def __repr__(self):
        return f"Manager({self.manager_email}, {self.manager_name})"   
         
class Category(DB.Model):
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Category({self.category_id}, {self.category_name})"
    
class Product(DB.Model):
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)   
    category_name = Column(String, nullable=False)
    product_description = Column(String(100), nullable=False)
    product_price = Column(Integer, nullable=False)
    product_stock = Column(Integer, nullable=False)
    product_unit = Column(String, nullable=False)

    category_id = Column(Integer, ForeignKey('category.category_id'), nullable=False)
    users = relationship('User', secondary='cart', back_populates='products')

    user_products = Table('cart', DB.metadata,
        Column('user_id', Integer, ForeignKey('user.user_id'), primary_key=True),
        Column('product_id', Integer, ForeignKey('product.product_id'), primary_key=True)
    )

    def __repr__(self):
        return f"Product({self.product_id}, {self.product_name})"
    
class Order(DB.Model):
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_quantity = Column(Integer, nullable=False)
    order_name = Column(String(), nullable=False)
    order_total =  Column(Integer, nullable=False)
    order_date = Column(String(16), default=date.today().strftime('%d-%m-%Y'))
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)

class Request(DB.Model):
    request_id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer)
    name = Column(String, nullable=False)
    request = Column(String(), nullable=False)
    status = Column(String(), default="Pending", nullable=False)
