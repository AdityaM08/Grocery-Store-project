from applications.celery_worker import celery, ContextTask
from applications.models import DB, User
from flask_restful import Api
from flask_cors import CORS
from flask import Flask
import os

def initate_app():
  app = Flask(__name__)
  CORS(app)
  base_dir = os.path.abspath(os.path.dirname(__file__))

  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(base_dir,"grocer_v2.sqlite3")
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SECRET_KEY'] = "CLASSIFIED"

  app.config["CACHE_TYPE"] = "redis"
  app.config['CACHE_REDIS_DB'] = 0
  app.config['CACHE_REDIS_HOST'] = "localhost"
  app.config['CACHE_REDIS_PORT'] = 6379
  app.config["CACHE_REDIS_URL"] = "redis://localhost:6379"  
  app.config['CACHE_DEFAULT_TIMEOUT'] = 300

  DB.init_app(app)
  api = Api(app)
  return app, api

app, api = initate_app()
app.app_context().push()

CELERY_BROKER_URL="redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND="redis://127.0.0.1:6379/2"

celery.conf.update(
    timezone="Asia/Kolkata",
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND
)

celery.Task = ContextTask

from applications.auth_api import *
api.add_resource(AdminLoginAPI, "/api/admin/login")
api.add_resource(ManagerSignupAPI, "/api/manager/signup")
api.add_resource(ManagerLoginAPI, "/api/manager/login")
api.add_resource(UserSignupAPI, "/api/user/signup")
api.add_resource(UserLoginAPI, "/api/user/login")

from applications.category_api import CategoryAPI
api.add_resource(CategoryAPI, "/api/category", "/api/category/<int:id>")

from applications.product_api import ProductAPI, DataExporterAPI
api.add_resource(ProductAPI, "/api/product", "/api/product/<int:id>")
api.add_resource(DataExporterAPI, "/api/product/export")

from applications.request_api import RequestAPI, ManagerRequestAPI, CategoryRequestAPI
api.add_resource(RequestAPI, "/api/request/category", "/api/request/category/<int:id>")
api.add_resource(ManagerRequestAPI, "/api/request/manager", "/api/request/manager/<int:id>")
api.add_resource(CategoryRequestAPI, "/api/category/request", "/api/category/request/<int:id>")

from applications.cart_api import CartAPI
api.add_resource(CartAPI, "/api/user/cart", "/api/user/cart/<int:id>")

from applications.purchase_api import PurchaseAPI, OrderAPI
api.add_resource(PurchaseAPI, "/api/user/cart/purchase")
api.add_resource(OrderAPI, "/api/user/orders")

def add_admin():
  admin = User.query.filter_by(role = 'admin').first()
  if not admin:
    new_admin = User(user_name="Administrator", 
                  user_email="admin@grocery.com", 
                  user_password= "2023", 
                  role='admin')
    DB.session.add(new_admin)
    DB.session.commit()
  print("Admin added successfully.")

if __name__ == '__main__':
  DB.create_all()
  add_admin()
  app.run(debug=True)