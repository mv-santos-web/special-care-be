from app import create_app
from app.extensions import db
from app.models.admin import Admin
from datetime import datetime

def create_admin():
    app = create_app()
    with app.app_context():
        # Dados do administrador
        admin_data = {
            'fullname': 'Admin do Sistema',
            'email': 'admin@specialcare.com',
            'phone': '11999999999',
            'cpf': '12345678901',  # CPF válido sem pontos e traço
            'birthdate': datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
            'gender': 'Masculino',  # Ou 'Feminino', 'Outro'
            'address': 'Endereço do administrador',
            'password': 'admin',  # Senha forte
            'type': 'admin'
        }
        
        # Verifica se já existe um admin com este email
        if Admin.query.filter_by(email=admin_data['email']).first():
            print('Já existe um administrador com este email!')
            return

        # Cria o administrador
        admin = Admin(**admin_data)
        admin.set_password(admin_data['password'])
        
        # Adiciona ao banco de dados
        db.session.add(admin)
        try:
            db.session.commit()
            print(f'Administrador {admin.fullname} criado com sucesso!')
        except Exception as e:
            db.session.rollback()
            print(f'Erro ao criar administrador: {str(e)}')

if __name__ == '__main__':
    create_admin()