from flask import request, current_app as app
from applications.models import DB, User, Manager
from datetime import datetime, timedelta
from flask_restful import abort, Resource
from functools import wraps
import jwt

def create_token(user_id, role):
    payload = {
        'id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=6) 
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return token.decode('utf-8')
    return token

def admin_role_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401, message='Token is not passed!') 
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['id']
            user = User.query.get(user_id)
            if user and user.role != 'admin':
                abort(403, message='Admin access required!')
        except (jwt.ExpiredSignatureError, jwt.DecodeError):          
            abort(401, message='Token is invalid!') 
        return f(*args, **kwargs)
    return decorated

def manager_role_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401, message='Token is not passed!')

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            manager_id = data['id']
            manager = Manager.query.get(manager_id)
            if not manager:
                abort(403, message='Manager access required!')
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            abort(401, message='Token is invalid!') 
        return f(*args, **kwargs)
    return decorated

def user_role_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401, message='Token is not passed!')
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['id']
            user = User.query.get(user_id)
            if user and user.role != 'user':
                abort(403, message='User access required!')
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            abort(401, message='Token is invalid!') 
        return f(*args, **kwargs)   
    return decorated

class AdminLoginAPI(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            abort(400, message="Please provide a valid email and password!")

        admin = User.query.filter_by(user_email=email.strip(), role="admin").first()
        if not admin:
            abort(400, message='Admin email does not match!') 

        if admin.user_password != password.strip():
            abort(400, message='Incorrect password! Please try again.') 

        DB.session.commit()
        return {
            'token': create_token(admin.user_id, "admin"),
            'message': 'Admin logged in successfully.'
        }, 200

class ManagerSignupAPI(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not email or not password or not name:
            abort(400, message="Please provide a valid email, name and password!")

        manager = Manager.query.filter_by(manager_email=email.strip()).first()
        if manager:
            abort(400, message='Email already exists!')

        new_manager = Manager(manager_name=name.strip(),
                              manager_email=email.strip(),
                              manager_password=password.strip(),)
        DB.session.add(new_manager)
        DB.session.commit()
        return {'message': 'request for manager account is sent successfully!'}, 201

class ManagerLoginAPI(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        manager = Manager.query.filter_by(manager_email=email.strip()).first()
        if not manager:
            abort(404, message='Email does not exist!')

        if manager.manager_password != password.strip():
            abort(400, message='Incorrect password')

        if manager.manager_status == 'Rejected':
            abort(400, message='Request for manager account is rejected!')

        elif manager.manager_status == 'Pending':
            abort(400, message='Request for manager account is pending!')
        
        return {
            'token': create_token(manager.manager_id, "manager"),
            'name': manager.manager_name.split()[0],
            'message': 'Manager logged in successfully.'
        }, 200
    

class UserSignupAPI(Resource):
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not email or not password or not name:
            abort(400, message="Please provide a valid email, name and password!")

        user = User.query.filter_by(user_email=email.strip()).first()

        if user:
            abort(400, message='Email already exists!')
        new_user = User(user_name=name.strip(),
                        user_email=email.strip(),
                        user_password=password.strip())
        DB.session.add(new_user)
        DB.session.commit()
        current_user = User.query.filter_by(user_email=email, role="user").first()
        return {
                'token': create_token(current_user.user_id, 'user'),
                'name': current_user.user_name.split()[0],
                'message': 'User account created successfully.'
               }, 201

class UserLoginAPI(Resource):    
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            abort(400, message="Please provide a valid email and password!")

        user = User.query.filter_by(user_email=email.strip(), role="user").first()
        if not user:
            abort(400, message='User email does not exist!') 

        if user.user_password != password.strip():
            abort(400, message='Incorrect password! Please try again.') 

        user.latest_log = datetime.utcnow()
        DB.session.commit()
        return {
            'token': create_token(user.user_id, "user"),
            'name': user.user_name.split()[0],
            'message': 'User logged in successfully.'
        }, 200