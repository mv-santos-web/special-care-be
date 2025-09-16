from pyhanko.sign import signers, PdfSigner, PdfSignatureMetadata
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from io import BytesIO
import hashlib
import datetime
from app.configs import Config
import os
from datetime import datetime
from weasyprint import HTML
from flask import render_template, url_for
import base64
import qrcode
import io

class PdfService:
    
    def __init__(self, app=None):
        self.upload_folder = Config.UPLOAD_FOLDER
        os.makedirs(self.upload_folder, exist_ok=True)
        self.app = app

    def init_app(self, app):
        self.app = app
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'recipes'), exist_ok=True)

    def generate_validation_code(self, patient_id, doctor_id, issue_date):
        """Gera um código de validação único para a receita"""
        timestamp = str(datetime.utcnow().timestamp())
        unique_string = f"{patient_id}_{doctor_id}_{issue_date}_{timestamp}"
        return hashlib.sha256(unique_string.encode()).hexdigest()

    def generate_pdf(self, recipe_data: dict) -> str:   
        """Gera um PDF a partir de um template HTML."""
        if not self.app:
            raise RuntimeError("Flask application not initialized. Call init_app first.")
            
        with self.app.app_context():
            # Add current time if not provided
            if 'issue_date' not in recipe_data:
                recipe_data['issue_date'] = datetime.now()
            
            # Add logo as base64
            logo_path = os.path.join(self.app.static_folder, 'images', 'logo.png')
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as image_file:
                    recipe_data['logo_data'] = base64.b64encode(image_file.read()).decode('utf-8')
                    
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=0,
            )
            validation_code = self.generate_validation_code(recipe_data['patient']['id'], recipe_data['medic']['id'], recipe_data['issue_date'])
            validation_url = "https://specialcaredev.pythonanywhere.com/validate_recipe/" + validation_code
            qr.add_data(validation_url)
            qr.make(fit=True)
            
            # Create an image from the QR Code instance
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes and then to base64
            buffered = io.BytesIO()
            qr_img.save(buffered, format="PNG")
            recipe_data['qr_code'] = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Render the template with Flask's render_template
            html_content = render_template(
                'prescription_template.html',
                **recipe_data
            )
            
            # Generate filename and path
            filename = f"recipe_{int(datetime.now().timestamp())}.pdf"
            recipes_dir = os.path.join(self.upload_folder, 'recipes')
            os.makedirs(recipes_dir, exist_ok=True)
            pdf_path = os.path.join(recipes_dir, filename)
            
            # Generate PDF
            HTML(string=html_content).write_pdf(pdf_path)
            
            return pdf_path, validation_code
    
    def sign_pdf(self, pdf_path: str, cert_path: str, password: str) -> str:
        """Signs a PDF using A1 certificate in PKCS#12 format (.p12 or .pfx)"""
        try:
            signer = signers.SimpleSigner.load_pkcs12(
                pfx_file=cert_path,
                passphrase=password.encode('utf-8')
            )

            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = IncrementalPdfFileWriter(pdf_file)
                metadata = PdfSignatureMetadata(field_name='Assinatura1')

                signed_pdf = BytesIO()
                pdf_signer = PdfSigner(metadata, signer=signer)
                pdf_signer.sign_pdf(pdf_reader, output=signed_pdf)
                signed_pdf.seek(0)
                
                pdf_file_signed = pdf_path.replace(".pdf", "_signed.pdf")

                with open(pdf_file_signed, 'wb+') as signed_file:
                    signed_file.write(signed_pdf.read())    
                
                return pdf_file_signed
        except Exception as error:
            print(f"Erro ao assinar o PDF: {str(error)}")
            raise error

    def create_medical_record_pdf(self, record: dict, logo_data: str) -> str:
        """Gera um PDF a partir de um template HTML."""
        
        if not self.app:
            raise RuntimeError("Flask application not initialized. Call init_app first.")
            
        with self.app.app_context():
            # Render the template with Flask's render_template
            html_content = render_template(
                'medical_record_template.html',
                record=record,
                current_time=datetime.now(),
                logo_data=logo_data
            )
            
            # Generate filename and path
            filename = f"medical_record_{int(datetime.now().timestamp())}.pdf"
            medical_records_dir = os.path.join(self.upload_folder, 'medical_records')
            os.makedirs(medical_records_dir, exist_ok=True)
            pdf_path = os.path.join(medical_records_dir, filename)
            
            # Generate PDF
            HTML(string=html_content).write_pdf(pdf_path)
            
            return pdf_path

