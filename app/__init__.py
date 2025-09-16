from flask import Flask
from datetime import datetime, timedelta

from app.configs import DevelopmentConfig
from app.extensions import init_extensions, migrate, db
from app.routes.medic import blueprint as medic_bp
from app.routes.nurse import blueprint as nurse_bp
from app.routes.admin import blueprint as admin_bp
from app.routes.api import blueprint as api_bp
from app.routes.public import blueprint as public_bp

from app.models import user, medic, patient, nurse, paramedic, medic_record, consult, prescription, emergency, nurse_request_emergency, nurse_request_consult


def register_template_filters(app):
    
    @app.template_filter('format_cpf')
    def format_cpf(cpf):
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if cpf else ""

    @app.template_filter('format_date')
    def format_date(date_obj):
        return date_obj.strftime('%d/%m/%Y') if date_obj else ""

    @app.template_filter('format_datetime')
    def format_datetime(datetime_obj):
        return datetime_obj.strftime('%d/%m/%Y %H:%M') if datetime_obj else ""

    @app.template_filter('add_days')
    def add_days(date_str, days):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return (date_obj + timedelta(days=days)).strftime('%d/%m/%Y')
        except:
            return ""
    
    @app.template_filter('format_issue_date')
    def format_issue_date(issue_date):
        return datetime.strptime(issue_date, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M') if issue_date else ""

    @app.template_filter('format_status')
    def format_status(status):
        return status.title() if status else ""
    
    @app.template_filter('format_status_emergency')
    def format_status_emergency(status):
        return status.title() if status else ""

def create_app():
    config = DevelopmentConfig  
    app = Flask(__name__)
    app.config.from_object(config)
    
    init_extensions(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(nurse_bp)
    app.register_blueprint(medic_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(public_bp)
    
    register_template_filters(app)
    
    return app



