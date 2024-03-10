from flask import request, current_app as app
from flask_restful import Resource, abort, marshal
from applications.models import DB, User, Product
from applications.auth_api import user_role_required
from applications.product_api import product_fields
from applications.category_api import cache
import jwt

class CartAPI(Resource):
    @user_role_required 
    @cache.cached(timeout=120)
    def get(self):
        data = jwt.decode(request.headers.get('Authorization'), app.config['SECRET_KEY'], algorithms=["HS256"])
        cart_products = []
        user = User.query.filter_by(user_id = data.get('id')).first()
        for product in marshal(user.products, product_fields):
            cart_products.append([product, 1])
        return {'cart_products': cart_products}, 200

    @user_role_required
    def post(self, id):
        data = jwt.decode(request.headers.get('Authorization'), app.config['SECRET_KEY'], algorithms=["HS256"])
        product = Product.query.filter_by(product_id = id).first()
        if not product:
            abort(404, message='Product not found!')

        user = User.query.filter_by(user_id = data.get('id')).first()
        if product not in user.products:
            user.products.append(product)
            DB.session.commit()
        cache.clear()
        return {'message': 'Product added to the cart!'}, 200