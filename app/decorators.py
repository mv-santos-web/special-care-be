from functools import wraps
from flask import jsonify
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.type != 'admin':
            return jsonify({"message": "Acesso negado: Apenas administradores podem acessar esta rota"}), 403
            
        return f(*args, **kwargs)
    return decorated_function

def nurse_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.type != 'nurse':
            return jsonify({"message": "Acesso negado: Apenas enfermeiros podem acessar esta rota"}), 403
            
        return f(*args, **kwargs)
    return decorated_function


def medic_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.type != 'medic':
            return jsonify({"message": "Acesso negado: Apenas medicos podem acessar esta rota"}), 403
            
        return f(*args, **kwargs)
    return decorated_function






