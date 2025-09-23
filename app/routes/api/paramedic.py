from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.paramedic_service import ParamedicService
from . import blueprint



@blueprint.route('/auth_paramedic', methods=['POST'])
def auth_paramedic():
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': 'Dados de autenticação não fornecidos'
        }), 400
        
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return jsonify({
            'success': False,
            'message': 'Email e senha são obrigatórios'
        }), 400
    
    try:
        paramedic = ParamedicService().auth_paramedic(email, password)
        if paramedic and paramedic.active:  
            access_token = create_access_token(identity=str(paramedic.id))
            return jsonify({
                'success': True,
                'access_token': access_token,
                'user': paramedic.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Credenciais inválidas ou usuário inativo'
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'message': str(e)
            }
        }), 404
        
@blueprint.route("/paramedics/data", methods=["GET"])
@jwt_required()
def get_paramedics_data():
    try:
        paramedic_service = ParamedicService()
        paramedics = paramedic_service.get_paramedics()
        return jsonify({"error": False, "message": "Paramedics fetched successfully", "data": paramedics})
    except Exception as e:
        print("Paramedics error: ", e)
        flash(f'Erro ao buscar paramédicos, {str(e)}.', 'error')
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/paramedics/me', methods=['GET'])
@jwt_required()
def get_paramedic_data():
    try:
        current_user_id = get_jwt_identity()
        paramedic_service = ParamedicService()
        paramedic = paramedic_service.get_paramedic(current_user_id)
        return jsonify(paramedic.to_dict())
    except Exception as e:
        print("Paramedic error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500
    
@blueprint.route('/paramedics/emergencies/data', methods=['GET'])
@jwt_required()
def get_emergencies_paramedic_data():
    try:
        current_user_id = get_jwt_identity()
        paramedic_service = ParamedicService()
        emergencies = paramedic_service.get_active_request_emergency(current_user_id)
        return jsonify(emergencies)
    except Exception as e:
        print("Emergencies error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/paramedics/emergencies/<int:emergency_id>/data', methods=['GET'])
@jwt_required()
def get_emergency_data_paramedic(emergency_id):
    try:
        current_user_id = get_jwt_identity()
        paramedic_service = ParamedicService()
        emergency = paramedic_service.get_emergency(emergency_id)
        return jsonify(emergency.to_dict())
    except Exception as e:
        print("Emergency error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500


@blueprint.route('/paramedics/emergencies/<int:emergency_id>/accept', methods=['GET'])
@jwt_required()
def accept_emergency_paramedic(emergency_id):
    try:
        current_user_id = get_jwt_identity()
        paramedic_service = ParamedicService()
        paramedic_service.accept_emergency(emergency_id, current_user_id)
        return jsonify({"error": False, "message": "Emergency accepted successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500


@blueprint.route('/paramedics/emergencies/<int:emergency_id>/finish', methods=['GET'])
@jwt_required()
def finish_emergency_paramedic(emergency_id):
    try:
        paramedic_service = ParamedicService()
        paramedic_service.finish_emergency(emergency_id)
        return jsonify({"error": False, "message": "Emergency finished successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/paramedics/emergencies/<int:emergency_id>/cancel', methods=['GET'])
@jwt_required()
def cancel_emergency_paramedic(emergency_id):
    try:
        paramedic_service = ParamedicService()
        paramedic_service.cancel_emergency(emergency_id)
        return jsonify({"error": False, "message": "Emergency canceled successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/paramedics/emergencies/<int:emergency_id>/arrived', methods=['GET'])
@jwt_required()
def arrived_emergency_paramedic(emergency_id):
    try:
        paramedic_service = ParamedicService()
        paramedic_service.arrived_emergency(emergency_id)
        return jsonify({"error": False, "message": "Emergency arrived successfully"})
    except Exception as e:
        print("Emergency error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/paramedics/update_location', methods=['POST'])
@jwt_required()
def update_location_paramedic():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        paramedic_service = ParamedicService()
        paramedic_service.update_location(current_user_id, data)
        return jsonify({"error": False, "message": "Location updated successfully"})
    except Exception as e:
        print("Location error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500

@blueprint.route('/paramedics/update_fcm_token', methods=['POST'])
@jwt_required()
def update_fcm_token_paramedic():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        paramedic_service = ParamedicService()
        paramedic_service.update_fcm_token(current_user_id, data)
        return jsonify({"error": False, "message": "FCM token updated successfully"})
    except Exception as e:
        print("FCM token error: ", e)
        return jsonify({"error": True, "message": str(e)}), 500







    
    