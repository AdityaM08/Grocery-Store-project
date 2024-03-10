from flask_restful import Resource, abort, marshal, fields
from flask import request, current_app as app
from sqlalchemy import func
from applications.batch_jobs import data_exporter
from applications.models import DB, Product, Category, Manager
from applications.auth_api import manager_role_required
from applications.category_api import cache
import jwt

product_fields = {
    'product_id': fields.Integer,
    'product_name': fields.String,
    'product_description': fields.String,
    'product_price': fields.Integer,
    'product_unit': fields.String,
    'product_stock': fields.Integer,
    'category_name': fields.String,
    'category_id': fields.Integer,
}
     
class ProductAPI(Resource):
    # @cache.cached(timeout=120)
    def get(self):
        args = request.args
        if args.get('q'):
            print(args.get('q'))
            query_string = f'%{args.get("q")}%'
            products = Product.query.filter(
                (func.lower(Product.product_name).like(query_string)) |
                (func.lower(Product.category_name).like(query_string)) |
                (func.lower(Product.product_description).like(query_string)) |
                (Product.product_price == args.get("q"))).all()
            print(products)
            return {'products' : marshal(products, product_fields)}, 200
    
        if args.get('id') and args.get('id').isdigit():
            product = Product.query.filter_by(product_id = int(args.get('id'))).first()
            if not product:
                abort(404, message="Product doesn't exist!")
            return {'product' : marshal(product, product_fields)}, 200
        products = Product.query.all()
        return {'products' : marshal(products, product_fields)}, 200
        
    @manager_role_required   
    def post(self, id):
        form_data = request.get_json()
        category = Category.query.filter_by(category_id=id).first()

        if not category:
            abort(404, message="Category doesn't exist!")
        
        product_name = form_data.get('name')
        product_description = form_data.get('description')
        product_stock = form_data.get('stock')
        product_price = form_data.get('price')
        product_unit = form_data.get('unit')

        if not product_name:
            abort(400, message="Please provide a valid product name!")

        if len(product_description) > 100:
            abort(400, message="Product description should be at most 100 charectors.")


        if not product_price or product_price <= 0:
            abort(400, message="Please provide a valid product price!")
        
        if not product_stock or product_stock <= 0:
            abort(400, message="Please provide a valid product price!")
        
        new_product = Product(product_name=product_name,
                              product_description=product_description,
                              product_stock=int(product_stock),
                              product_price=int(product_price),
                              product_unit=product_unit,
                              category_name=category.category_name,
                              category_id=category.category_id)
        DB.session.add(new_product)
        DB.session.commit()
        cache.clear()
        return {"message": "Product added successfully!"}, 201

    @manager_role_required
    def put(self, id):
        form_data = request.get_json()
        product = Product.query.filter_by(product_id=id).first()
        if not product:
            abort(404, message="Product doesn't exist!")
        
        product_name = form_data.get('name')
        product_description = form_data.get('description')
        product_stock = form_data.get('stock')
        product_price = form_data.get('price')
        product_unit = form_data.get('unit')

        if not product_name:
            abort(400, message="Please provide a valid product name!")

        if len(product_description) > 100:
            abort(400, message="Product description should be at most 100 charectors.")


        if not product_price or product_price <= 0:
            abort(400, message="Please provide a valid product price!")
        
        if not product_stock or product_stock <= 0:
            abort(400, message="Please provide a valid product price!")

        product.product_name=product_name
        product.product_description=product_description
        product.product_stock=int(product_stock)
        product.product_price=int(product_price)
        product.product_unit=product_unit

        DB.session.commit()
        cache.clear()
        return {"message": "Product updated successfully!"}, 200

    @manager_role_required   
    def delete(self, id):
        product = Product.query.filter_by(product_id=id).first()
        if not product:
            abort(404, message="Product doesn't exist!")

        DB.session.delete(product)
        DB.session.commit()
        cache.clear()
        return {"message": "Product deleted successfully!"}, 200
    
    
class DataExporterAPI(Resource):
    @manager_role_required
    def get(self):
        data = jwt.decode(request.headers.get('Authorization'), app.config['SECRET_KEY'], algorithms=["HS256"])

        manager = Manager.query.filter_by(manager_id = data.get('id')).first()
        products = Product.query.all()
        product_details = []
        for product in products:
            product_details.append([product.product_name, 
                                    product.category_name,
                                    product.product_description, 
                                    product.product_price, 
                                    product.product_unit, 
                                    product.product_stock])
        email =  manager.manager_email
        name =  manager.manager_name.split()[0]   
        data_exporter(product_details, email, name)
        return {'message': 'Product details sent to mail.'}, 200
    