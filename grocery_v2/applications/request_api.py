from flask_restful import Resource, abort, marshal, fields
from applications.models import DB, Category, Manager, Request, Product
from applications.auth_api import admin_role_required, manager_role_required
from applications.category_api import cache
from flask import request

manager_fields = {
    'manager_id': fields.Integer,
    'manager_name': fields.String,
    'manager_email': fields.String,
    'manager_status': fields.String,
}

request_fields = {
    'request_id': fields.Integer,
    'category_id': fields.Integer,
    'name': fields.String,
    'request': fields.String,
    'status': fields.String,
}

class ManagerRequestAPI(Resource):
    @admin_role_required 
    @cache.memoize(timeout=300)
    def get(self):
        manager_requests = Manager.query.all()
        return {'manager_requests': marshal(manager_requests, manager_fields)}, 200
    
    def post(self, id):
        if 'action' not in request.args or request.args.get('action') not in ['approve', 'reject']:
            abort(400, message='Please provide a valid action!')

        manager = Manager.query.filter_by(manager_status='Pending', manager_id=id).first()
        if not manager:
            abort(404, message='Manager request not found!')

        action = request.args.get('action')
        if action == 'approve':
            manager.manager_status = 'Approved'
            DB.session.commit()
            cache.clear()
            return {'message': 'Manager approved successfully!'}, 200
        manager.manager_status = 'Rejected'
        DB.session.commit()
        cache.clear()
        return {'message': 'Manager rejected successfully!'}, 200
    

class CategoryRequestAPI(Resource):
    @manager_role_required 
    def post(self):
        form_data = request.get_json()
        name = form_data.get('category')
        if not name:
            abort(400, message="Please enter a valid category name!")

        new_category_request = Request(name=name.strip(), request='Create Category')
        DB.session.add(new_category_request)
        DB.session.commit()
        cache.clear()
        return {'message': 'Category request sent.'}, 201

    @manager_role_required
    def put(self, id):
        category = Category.query.filter_by(category_id=id).first()
        if not category:
            abort(404, message="Category doesn't exist!")

        form_data = request.get_json()
        name = form_data.get('category')
        if not name:
            abort(400, message="Please enter a valid category name!")

        new_category_request = Request(name=name.strip(), 
                                       request='Edit Category', 
                                       category_id=category.category_id)
        DB.session.add(new_category_request)
        DB.session.commit()
        cache.clear()
        return {'message': 'Category request sent.'}, 200
    
    @manager_role_required
    def delete(self, id):
        category = Category.query.filter_by(category_id=id).first()
        if not category:
            abort(404, message="Category doesn't exist!")

        new_category_request = Request(name=category.category_name, 
                                       request='Delete Category', 
                                       category_id=category.category_id)
        DB.session.add(new_category_request)
        DB.session.commit()
        cache.clear()
        return {'message': 'Category request sent.'}, 200
    
class RequestAPI(Resource):
    @admin_role_required 
    @cache.memoize(timeout=300)
    def get(self):
        category_requests = Request.query.all()
        return {'category_requests': marshal(category_requests, request_fields)}, 200
    
    def post(self, id):
        if 'action' not in request.args or request.args.get('action') not in ['approve', 'reject']:
            abort(400, message='Please provide a valid action!')    

        category_request = Request.query.filter_by(request_id=id, status='Pending').first()
        if not category_request:
            abort(404, message="Request not found!")

        action = request.args.get('action')
        if action == 'approve':
            if category_request.request == 'Create Category':
                new_category = Category(category_name=category_request.name)
                DB.session.add(new_category)
                category_request.status = 'Approved'
                DB.session.commit()
                cache.clear()
                return {'message': 'Category request approved!'}, 200
            
            elif category_request.request == 'Edit Category':
                category = Category.query.filter_by(category_id=category_request.category_id).first()
                if category:
                    category.category_name = category_request.name
                    products = Product.query.filter_by(category_id = category_request.category_id).all()
                    for product in products:
                        product.category_name = category_request.name
                    category_request.status = 'Approved'
                    DB.session.commit()
                    cache.clear()
                    return {'message': 'Category request approved!'}, 200
                
            elif category_request.request == 'Delete Category':
                Category.query.filter_by(category_id = category_request.category_id).delete()
                category_request.status = 'Approved'
                DB.session.commit()
                cache.clear()
                return {'message': 'Category request approved!'}, 200
            
        elif action == 'reject':    
            category_request.status = 'Rejected'
            DB.session.commit()
            cache.clear()
            return {'message': 'Category request rejected!'}, 200