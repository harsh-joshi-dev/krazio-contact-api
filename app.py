from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import re

# Load environment variables (silently fail if .env doesn't exist)
try:
    load_dotenv()
except Exception:
    pass  # .env file is optional, environment variables can be set directly

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Log startup (this helps debug)
import sys
print("Flask app initialized", file=sys.stderr)
sys.stderr.flush()

# Email configuration from environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', 'krazio.developers@gmail.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'scoq vbap nqhx dlyj')
FROM_EMAIL = os.getenv('FROM_EMAIL', SMTP_USERNAME)
TO_EMAIL = os.getenv('TO_EMAIL', 'krazio.developers@gmail.com')  # Email address to receive contact form submissions


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number format (basic validation)"""
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it contains only digits and optional + at start
    return re.match(r'^\+?\d{10,15}$', cleaned) is not None


def create_user_confirmation_email_html(name, company):
    """Create HTML email template for user confirmation"""
    company_text = f" at {company}" if company else ""
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Thank You for Contacting Us</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f4f4f4;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f4f4f4;">
            <tr>
                <td style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden;">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; letter-spacing: -0.5px;">
                                    Thank You, {name}!
                                </h1>
                            </td>
                        </tr>
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="margin: 0 0 20px 0; color: #333333; font-size: 16px; line-height: 1.6;">
                                    We've received your message and truly appreciate you taking the time to reach out to us{company_text}.
                                </p>
                                <p style="margin: 0 0 20px 0; color: #333333; font-size: 16px; line-height: 1.6;">
                                    Our team is currently reviewing your inquiry and will get back to you as soon as possible, typically within 24-48 hours.
                                </p>
                                <div style="background-color: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; margin: 30px 0; border-radius: 4px;">
                                    <p style="margin: 0; color: #555555; font-size: 14px; line-height: 1.6;">
                                        <strong style="color: #333333;">What happens next?</strong><br>
                                        We'll review your message and respond to the email address you provided. If your inquiry is urgent, please don't hesitate to reach out to us directly.
                                    </p>
                                </div>
                                <p style="margin: 30px 0 0 0; color: #333333; font-size: 16px; line-height: 1.6;">
                                    We look forward to connecting with you soon!
                                </p>
                                <p style="margin: 30px 0 0 0; color: #333333; font-size: 16px; line-height: 1.6;">
                                    Best regards,<br>
                                    <strong style="color: #667eea;">The Krazio Team</strong>
                                </p>
                            </td>
                        </tr>
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e9ecef;">
                                <p style="margin: 0 0 10px 0; color: #6c757d; font-size: 12px; line-height: 1.5;">
                                    This is an automated confirmation email. Please do not reply to this message.
                                </p>
                                <p style="margin: 0; color: #6c757d; font-size: 12px; line-height: 1.5;">
                                    © {os.getenv('COMPANY_NAME', 'Krazio')} - All rights reserved
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


def create_admin_notification_email_html(name, phone, business_email, company, message):
    """Create HTML email template for admin notification"""
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🔥 New Lead - {name}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f4f4f4;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f4f4f4;">
            <tr>
                <td style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); overflow: hidden; border: 2px solid #667eea;">
                        <!-- Header -->
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                                <div style="display: inline-block; background-color: rgba(255, 255, 255, 0.2); padding: 8px 16px; border-radius: 20px; margin-bottom: 10px;">
                                    <span style="color: #ffffff; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">🔥 NEW LEAD</span>
                                </div>
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; letter-spacing: -0.5px;">
                                    New Lead Received
                                </h1>
                            </td>
                        </tr>
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px 30px;">
                                <p style="margin: 0 0 30px 0; color: #333333; font-size: 16px; line-height: 1.6;">
                                    <strong style="color: #667eea;">Action Required:</strong> You have received a new lead that requires your attention:
                                </p>
                                
                                <table role="presentation" style="width: 100%; border-collapse: collapse; margin: 30px 0;">
                                    <tr>
                                        <td style="padding: 15px; background-color: #f8f9fa; border-bottom: 1px solid #e9ecef;">
                                            <strong style="color: #667eea; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Name</strong>
                                        </td>
                                        <td style="padding: 15px; background-color: #ffffff; border-bottom: 1px solid #e9ecef;">
                                            <span style="color: #333333; font-size: 16px;">{name}</span>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 15px; background-color: #f8f9fa; border-bottom: 1px solid #e9ecef;">
                                            <strong style="color: #667eea; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Email</strong>
                                        </td>
                                        <td style="padding: 15px; background-color: #ffffff; border-bottom: 1px solid #e9ecef;">
                                            <a href="mailto:{business_email}" style="color: #667eea; font-size: 16px; text-decoration: none;">{business_email}</a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding: 15px; background-color: #f8f9fa; border-bottom: 1px solid #e9ecef;">
                                            <strong style="color: #667eea; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Phone</strong>
                                        </td>
                                        <td style="padding: 15px; background-color: #ffffff; border-bottom: 1px solid #e9ecef;">
                                            <a href="tel:{phone}" style="color: #333333; font-size: 16px; text-decoration: none;">{phone}</a>
                                        </td>
                                    </tr>
                                    {f'''<tr>
                                        <td style="padding: 15px; background-color: #f8f9fa; border-bottom: 1px solid #e9ecef;">
                                            <strong style="color: #667eea; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Company</strong>
                                        </td>
                                        <td style="padding: 15px; background-color: #ffffff; border-bottom: 1px solid #e9ecef;">
                                            <span style="color: #333333; font-size: 16px;">{company}</span>
                                        </td>
                                    </tr>''' if company else ''}
                                </table>
                                
                                <div style="background-color: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; margin: 30px 0; border-radius: 4px;">
                                    <p style="margin: 0 0 10px 0; color: #667eea; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                                        Message
                                    </p>
                                    <p style="margin: 0; color: #333333; font-size: 16px; line-height: 1.8; white-space: pre-wrap;">{message}</p>
                                </div>
                                
                                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e9ecef;">
                                    <a href="mailto:{business_email}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; padding: 12px 30px; border-radius: 6px; font-weight: 600; font-size: 14px;">
                                        Reply to {name}
                                    </a>
                                </div>
                            </td>
                        </tr>
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #f8f9fa; padding: 20px 30px; text-align: center; border-top: 1px solid #e9ecef;">
                                <p style="margin: 0 0 5px 0; color: #667eea; font-size: 12px; font-weight: 600; line-height: 1.5;">
                                    ⚡ High Priority Lead - Please Respond Promptly
                                </p>
                                <p style="margin: 0; color: #6c757d; font-size: 12px; line-height: 1.5;">
                                    This email was automatically generated from your contact form.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html


def send_admin_notification(name, phone, business_email, company, message):
    """Send HTML email notification to admin with high priority"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = FROM_EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = f'🔥 New Lead - {name}'
        
        # Set email priority to High/Urgent
        msg['X-Priority'] = '1'  # 1 = High, 3 = Normal, 5 = Low
        msg['Priority'] = 'urgent'
        msg['Importance'] = 'high'
        
        # Create HTML email
        html_content = create_admin_notification_email_html(name, phone, business_email, company, message)
        
        # Create plain text fallback
        text_content = f"""
🔥 NEW LEAD - ACTION REQUIRED

You have received a new lead that requires your attention:

Name: {name}
Phone Number: {phone}
Business Email: {business_email}
Company: {company if company else 'Not provided'}
Message:
{message}

---
This is a high-priority lead notification from the Contact Us form.
Please respond promptly to this lead.
        """
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable encryption
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True, "Admin notification sent successfully"
    
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP authentication failed. Please check your email credentials."
    except smtplib.SMTPException as e:
        return False, f"SMTP error occurred: {str(e)}"
    except Exception as e:
        return False, f"An error occurred while sending email: {str(e)}"


def send_user_confirmation(name, business_email, company):
    """Send HTML confirmation email to user"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = FROM_EMAIL
        msg['To'] = business_email
        msg['Subject'] = 'Thank You for Contacting Us - We\'ll Be In Touch Soon!'
        
        # Create HTML email
        html_content = create_user_confirmation_email_html(name, company)
        
        # Create plain text fallback
        text_content = f"""
Thank You, {name}!

We've received your message and truly appreciate you taking the time to reach out to us{f' at {company}' if company else ''}.

Our team is currently reviewing your inquiry and will get back to you as soon as possible, typically within 24-48 hours.

What happens next?
We'll review your message and respond to the email address you provided. If your inquiry is urgent, please don't hesitate to reach out to us directly.

We look forward to connecting with you soon!

Best regards,
The Krazio Team

---
This is an automated confirmation email. Please do not reply to this message.
        """
        
        # Attach both plain text and HTML versions
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Enable encryption
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        
        return True, "User confirmation sent successfully"
    
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP authentication failed. Please check your email credentials."
    except smtplib.SMTPException as e:
        return False, f"SMTP error occurred: {str(e)}"
    except Exception as e:
        return False, f"An error occurred while sending email: {str(e)}"


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Contact Us API',
        'version': '1.0.0',
        'endpoints': {
            'health': 'GET /health',
            'contact': 'POST /api/contact',
            'contact_alt': 'POST /contact'
        },
        'status': 'running'
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint - must respond quickly"""
    return jsonify({
        'status': 'healthy',
        'message': 'Contact API is running'
    }), 200


@app.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint for health checks"""
    return jsonify({'pong': True}), 200


@app.route('/contact', methods=['POST'])
@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        business_email = data.get('business_email', '').strip()
        company = data.get('company', '').strip()  # Optional
        message = data.get('message', '').strip()
        
        # Validate required fields
        if not name:
            return jsonify({
                'success': False,
                'message': 'Name is required'
            }), 400
        
        if not phone:
            return jsonify({
                'success': False,
                'message': 'Phone number is required'
            }), 400
        
        if not business_email:
            return jsonify({
                'success': False,
                'message': 'Business email is required'
            }), 400
        
        if not message:
            return jsonify({
                'success': False,
                'message': 'Message is required'
            }), 400
        
        # Validate email format
        if not validate_email(business_email):
            return jsonify({
                'success': False,
                'message': 'Invalid business email format'
            }), 400
        
        # Validate phone format
        if not validate_phone(phone):
            return jsonify({
                'success': False,
                'message': 'Invalid phone number format'
            }), 400
        
        # Send admin notification email
        admin_success, admin_message = send_admin_notification(name, phone, business_email, company, message)
        
        # Send user confirmation email
        user_success, user_message = send_user_confirmation(name, business_email, company)
        
        # Check if both emails were sent successfully
        if admin_success and user_success:
            return jsonify({
                'success': True,
                'message': 'Contact form submitted successfully. A confirmation email has been sent to your business email. We will get back to you soon!'
            }), 200
        elif admin_success:
            # Admin email sent but user confirmation failed
            return jsonify({
                'success': True,
                'message': 'Contact form submitted successfully. However, we were unable to send a confirmation email. We will still get back to you soon!',
                'warning': 'Confirmation email failed to send'
            }), 200
        else:
            # Admin email failed
            return jsonify({
                'success': False,
                'message': f'Failed to send email: {admin_message}'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }), 500


# Validate configuration (only print warnings, don't block startup)
if not SMTP_USERNAME or not SMTP_PASSWORD:
    print("WARNING: SMTP_USERNAME and SMTP_PASSWORD are not set in environment variables.")
    print("Please set them in .env file or as environment variables.")

if not TO_EMAIL:
    print("WARNING: TO_EMAIL is not set. Contact form emails will not be sent anywhere.")

if __name__ == '__main__':
    # Get port from environment variable (Render provides PORT, default to 5001 for local)
    port = int(os.getenv('PORT', 5001))
    # Only enable debug mode in development
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)

