from flask import request, current_app as app
from flask_restful import Resource, marshal, fields
from applications.models import DB, User, Product, Order
from applications.auth_api import user_role_required
from applications.category_api import cache
import jwt

order_fields = {
    'order_id': fields.Integer,
    'order_quantity': fields.Integer,
    'order_name': fields.String,
    'order_total': fields.Integer,
    'order_date': fields.String,
    'user_id': fields.Integer,
}

class PurchaseAPI(Resource):
    @user_role_required
    def post(self):
        data = jwt.decode(request.headers.get('Authorization'), app.config['SECRET_KEY'], algorithms=["HS256"])
        user = User.query.filter_by(user_id = data.get('id')).first()
        form_data = request.form

        for product_id, quantity in form_data.items():
            product = Product.query.filter_by(product_id=int(product_id)).first()

            if product:
                if product.product_stock >= int(quantity):
                    order_total = product.product_price * int(quantity)
                    new_order = Order(order_name=product.product_name,
                                    order_total=order_total,
                                    order_quantity=int(quantity),
                                    user_id=data.get('id'))
                    
                    product.product_stock -= int(quantity)
                    DB.session.add(new_order)
                user.products.remove(product)
        DB.session.commit()
        cache.clear()
        return {'message': 'Thank you for shopping.'}, 200

class OrderAPI(Resource):
    @user_role_required
    @cache.cached(timeout=120)
    def get(self):
        data = jwt.decode(request.headers.get('Authorization'), app.config['SECRET_KEY'], algorithms=["HS256"])
        orders = Order.query.filter_by(user_id = data.get('id')).all()
        return {'orders': marshal(orders, order_fields)}