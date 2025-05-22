from flask import Blueprint, request, jsonify
from models import db, User

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'message': 'Servicio de autenticación funcionando correctamente', 
        'status': 'ok'
    }), 200

@routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No se recibieron datos JSON'}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({
                'message': 'Faltan datos: username, email y password son requeridos'
            }), 400
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'El usuario ya existe'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'El email ya está registrado'}), 400
        
        # Crear nuevo usuario
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': 'Usuario creado correctamente'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error interno del servidor: {str(e)}'}), 500

@routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'message': 'No se recibieron datos JSON'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email y password son requeridos'}), 400
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            return jsonify({
                'message': 'Login exitoso',
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }), 200
        
        return jsonify({'message': 'Usuario o contraseña incorrecta'}), 401
        
    except Exception as e:
        return jsonify({'message': f'Error interno del servidor: {str(e)}'}), 500

@routes.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_list = []
        
        for user in users:
            users_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email
            })
        
        return jsonify({
            'users': users_list,
            'total': len(users_list)
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error interno del servidor: {str(e)}'}), 500