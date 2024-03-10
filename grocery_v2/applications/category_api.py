from flask_restful import Resource, abort, marshal, fields
from applications.models import Category, Product, DB
from applications.auth_api import admin_role_required
from flask import request, current_app as app
from flask_caching import Cache

cache = Cache(app)

category_fields = {
    'category_id': fields.Integer,
    'category_name': fields.String,
}

class CategoryAPI(Resource):
    @admin_role_required
    # @cache.cached(timeout=120)
    def get(self):
        args = request.args    
        if args.get('id') and args.get('id').isdigit():
            category = Category.query.filter_by(category_id = int(args.get('id'))).first()
            if not category:
                abort(404, message="Category doesn't exist!")
            return {'category': marshal(category, category_fields)}, 200
        categories = Category.query.all()
        return {'categories': marshal(categories, category_fields)}, 200

    @admin_role_required
    def post(self):
        form_data = request.get_json()       
        name = form_data.get('category')

        if not name:
            abort(400, message="Please enter a valid category name!")

        new_category = Category(category_name=name.strip())
        DB.session.add(new_category)
        DB.session.commit()
        cache.clear()
        return {"message": "Category added successfully!"}, 201

    @admin_role_required
    def put(self, id):
        form_data = request.get_json()       
        name = form_data.get('category')

        if not name:
            abort(400, message="Please enter a valid category name!")

        category = Category.query.filter_by(category_id=id).first()
        if not category:
            abort(404, message="Category doesn't exist!")
        
        category.category_name = name.strip()
        products = Product.query.filter_by(category_id = id).all()
        for product in products:
            product.category_name = name.strip()
        DB.session.commit()
        cache.clear()
        return {"message": "Category updated successfully!"}, 200

    @admin_role_required
    def delete(self, id):
        category = Category.query.filter_by(category_id=id).first()
        if not category:
            abort(404, message="Category doesn't exist!")

        DB.session.delete(category)
        DB.session.commit()
        cache.clear()
        return {"message": "Category deleted successfully!"}, 200
    