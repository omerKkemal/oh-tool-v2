# File: utility/email_temp.py
# -*- coding: utf-8 -*-
"""
SpecterPanel - Email Templates
Safe external email sending with HTML templates and plain-text fallback.
White & Gold Theme Edition - Email Client Compatible
"""
from string import Template
import smtplib
from email.message import EmailMessage
from datetime import datetime
import re
import logging
import traceback

from utility.setting import Setting

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Setting()
config.setting_var()

class EmailTemplate:
    def __init__(self):
        # Use Template to avoid { } conflicts in CSS
        self.HTML_TEMP = Template(self._build_template())

    def _build_template(self):
        return '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>SpecterPanel Notification</title>
                <style type="text/css">
                    /* Reset for email clients */
                    .ExternalClass { width: 100%; }
                    .ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div { line-height: 100%; }
                    body { margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
                    table { border-collapse: collapse; mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
                    img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic; }
                    p { display: block; margin: 13px 0; }
                </style>
                <!--[if mso]>
                <style type="text/css">
                    .body-table { width: 600px !important; }
                </style>
                <![endif]-->
            </head>
            <body style="margin: 0; padding: 0; background-color: #f8f9fa; font-family: Arial, sans-serif;">
                <!--[if mso]>
                <center>
                <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" class="body-table">
                <tr>
                <td>
                <![endif]-->
                
                <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border: 2px solid #d4af37; border-radius: 0; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <!-- Gold Header -->
                    <tr>
                        <td align="center" bgcolor="#d4af37" style="padding: 30px; background: linear-gradient(135deg, #d4af37 0%, #f7ef8a 100%);">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center" style="color: #1a1a1a; font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
                                        SPECTERPANEL
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" style="color: #1a1a1a; font-family: Arial, sans-serif; font-size: 14px; font-weight: 600; padding-top: 8px; opacity: 0.9;">
                                        PREMIUM SECURITY NOTIFICATION SYSTEM
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- White Content Area -->
                    <tr>
                        <td style="padding: 40px 30px;" bgcolor="#ffffff">
                            $content
                        </td>
                    </tr>
                    
                    <!-- Gold Footer -->
                    <tr>
                        <td align="center" bgcolor="#f8f9fa" style="padding: 25px; border-top: 2px solid #d4af37;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td align="center" style="color: #666666; font-family: Arial, sans-serif; font-size: 13px; line-height: 1.5;">
                                        &copy; 2024 SpecterPanel Security System. All rights reserved.<br>
                                        This is an automated message. Please do not reply to this email.
                                    </td>
                                </tr>
                                <tr>
                                    <td align="center" style="padding-top: 15px;">
                                        <span style="display: inline-block; background-color: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37; border-radius: 20px; padding: 8px 20px; color: #8b6e1f; font-family: Arial, sans-serif; font-size: 12px; font-weight: 600;">
                                            🛡️ Premium Encrypted Communication
                                        </span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
                
                <!--[if mso]>
                </td>
                </tr>
                </table>
                </center>
                <![endif]-->
            </body>
            </html>
        '''

    def _inline_styles(self, content):
        """Convert CSS classes to inline styles for email compatibility"""
        styles_map = {
            'class="status-indicator"': 'style="display: inline-block; background-color: rgba(212, 175, 55, 0.1); border: 2px solid #d4af37; border-radius: 25px; padding: 10px 20px; color: #8b6e1f; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; margin: 15px 0; text-transform: uppercase; letter-spacing: 0.5px;"',
            'class="message-box"': 'style="background-color: #fefefe; border-left: 4px solid #d4af37; border: 2px solid #f0f0f0; padding: 25px; margin: 25px 0; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);"',
            'class="btn-container"': 'style="text-align: center; margin: 30px 0 20px;"',
            'class="btn"': 'style="display: inline-block; background: linear-gradient(135deg, #d4af37 0%, #f7ef8a 100%); color: #1a1a1a; text-decoration: none; padding: 16px 36px; font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; border-radius: 6px; margin: 10px 0; border: none; box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);"',
            'class="info-grid"': 'style="margin: 25px 0;"',
            'class="info-item"': 'style="background-color: #f8f9fa; border: 2px solid #e9ecef; border-left: 4px solid #d4af37; padding: 20px; margin-bottom: 15px; border-radius: 6px;"',
            'class="info-label"': 'style="color: #8b6e1f; font-family: Arial, sans-serif; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;"',
            'class="info-value"': 'style="color: #2d2d2d; font-family: Arial, sans-serif; font-size: 16px; font-weight: bold;"',
            'class="warning"': 'style="background-color: rgba(212, 175, 55, 0.08); border-left: 4px solid #d4af37; padding: 16px 20px; margin: 20px 0; color: #8b6e1f; font-family: Arial, sans-serif; font-size: 14px; border-radius: 6px; border: 1px solid rgba(212, 175, 55, 0.2);"',
            'class="terminal-container"': 'style="margin: 25px 0;"',
            'class="terminal"': 'style="background-color: #2d2d2d; border: 2px solid #d4af37; border-radius: 8px; font-family: Courier New, monospace; overflow: hidden;"',
            'class="terminal-header"': 'style="background-color: #3d3d3d; padding: 15px 20px; border-bottom: 2px solid #d4af37;"',
            'class="terminal-body"': 'style="padding: 20px; color: #ffffff; font-family: Courier New, monospace; font-size: 14px; line-height: 1.5;"',
            'class="prompt"': 'style="color: #d4af37; font-weight: bold;"',
            'class="command"': 'style="color: #ffffff; font-weight: 500;"',
            'class="output"': 'style="color: #b0b0b0;"',
            'class="feature-grid"': 'style="margin: 25px 0;"',
            'class="feature-item"': 'style="background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; margin-bottom: 12px; border-radius: 6px; border-left: 3px solid #d4af37;"',
        }
        
        for class_name, inline_style in styles_map.items():
            content = content.replace(class_name, inline_style)
        
        return content

    # ===== Validation Methods =====
    def validate_email(self, email):
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def sanitize_input(self, text):
        """Basic input sanitization for email content"""
        if not text:
            return ""
        # Remove potentially dangerous characters
        sanitized = str(text).replace('<script>', '').replace('</script>', '')
        return sanitized[:1000]  # Limit length

    def check_smtp_config(self):
        """Check if SMTP configuration is valid"""
        try:
            with smtplib.SMTP(config.SMTP_LINK, config.SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(config.EMAIL, config.EMAIL_PASSWORD)
                logger.info("✅ SMTP configuration is valid")
                return True
        except Exception as e:
            logger.error(f"❌ SMTP configuration error: {e}")
            return False

    # ===== Email templates =====
    def user_notify(self, email):
        """Welcome New user registration email template"""
        safe_email = self.sanitize_input(email)
        
        content = f'''
            <h1 style="color: #d4af37; font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; margin-bottom: 20px; text-align: center;">Welcome to SpecterPanel</h1>

            <div class="status-indicator">PREMIUM REGISTRATION SUCCESSFUL</div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">Dear User,</p>
            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">Welcome to SpecterPanel! Your account has been successfully created and is now active with premium access.</p>

            <div class="message-box">
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 12px; font-size: 15px;"><strong style="color: #d4af37;">Account Email:</strong> {safe_email}</p>
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 12px; font-size: 15px;"><strong style="color: #d4af37;">Registration Time:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 0; font-size: 15px;"><strong style="color: #d4af37;">Access Level:</strong> <span style="color: #d4af37; font-weight: bold;">PREMIUM</span></p>
            </div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">You can now log in to your dashboard and start using all premium features.</p>

            <div class="btn-container">
                <a href="https://www.mylink.com/login" class="btn">Access Premium Dashboard</a>
            </div>

            <!-- Terminal Demo -->
            <div class="terminal-container">
                <div class="terminal">
                    <div class="terminal-header">
                        <table width="100%">
                            <tr>
                                <td>
                                    <span style="color: #d4af37; font-family: Courier New, monospace; font-size: 13px; font-weight: bold;">specterpanel@server:~</span>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div class="terminal-body">
                        <div style="margin-bottom: 10px;">
                            <span class="prompt">user@specterpanel:~$ </span>
                            <span class="command">connect target-7842</span>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <span class="output">✅ Connected to target-7842 (Linux Ubuntu 22.04)</span>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <span class="prompt">user@specterpanel:~$ </span>
                            <span class="command">status check</span>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <span class="output">📊 System Status: <span style="color: #d4af37;">OPERATIONAL</span></span>
                        </div>
                        <div style="margin-bottom: 10px;">
                            <span class="output">🖥️ CPU Usage: 24% | 💾 Memory: 3.2/8GB</span>
                        </div>
                        <div style="margin-bottom: 0;">
                            <span class="output">🌐 Network: Active | 🔒 Security: <span style="color: #d4af37;">ENABLED</span></span>
                        </div>
                    </div>
                </div>
            </div>

            <h2 style="color: #d4af37; font-family: Arial, sans-serif; font-size: 22px; font-weight: bold; margin: 30px 0 20px 0; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;">Premium Features</h2>

            <div class="feature-grid">
                <div class="feature-item">
                    <h3 style="color: #d4af37; font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; margin: 0 0 8px 0;">🎯 Advanced Target Management</h3>
                    <p style="color: #666666; font-family: Arial, sans-serif; font-size: 14px; margin: 0; line-height: 1.5;">Monitor and manage all connected devices with precision and real-time analytics.</p>
                </div>
                
                <div class="feature-item">
                    <h3 style="color: #d4af37; font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; margin: 0 0 8px 0;">⚡ Real-Time Command Execution</h3>
                    <p style="color: #666666; font-family: Arial, sans-serif; font-size: 14px; margin: 0; line-height: 1.5;">Execute commands instantly across your network with secure, encrypted communication.</p>
                </div>
                
                <div class="feature-item">
                    <h3 style="color: #d4af37; font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; margin: 0 0 8px 0;">📊 Comprehensive Analytics</h3>
                    <p style="color: #666666; font-family: Arial, sans-serif; font-size: 14px; margin: 0; line-height: 1.5;">Gain insights with detailed reports and visual analytics on system performance.</p>
                </div>
            </div>

            <div class="warning">
                💫 You now have access to all premium features. Explore the dashboard to get started!
            </div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">We're excited to have you on board!</p>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 15px; margin-bottom: 0; line-height: 1.6;">Best Regards,<br><strong style="color: #d4af37;">The SpecterPanel Team</strong></p>
        '''

        # Apply inline styles for email compatibility
        content = self._inline_styles(content)
        final_content = self.HTML_TEMP.safe_substitute(content=content)
        return final_content

    def new_user(self, email):
        """Notify admin about new user registration"""
        safe_email = self.sanitize_input(email)
        
        content = f'''
            <h1 style="color: #d4af37; font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; margin-bottom: 20px; text-align: center;">New User Registration</h1>

            <div class="status-indicator">NEW ACCOUNT ALERT</div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">Dear Administrator,</p>
            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">A new user has registered for SpecterPanel and requires your attention.</p>

            <div class="message-box">
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 12px; font-size: 15px;"><strong style="color: #d4af37;">User Email:</strong> {safe_email}</p>
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 12px; font-size: 15px;"><strong style="color: #d4af37;">Registration Time:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 0; font-size: 15px;"><strong style="color: #d4af37;">Status:</strong> <span style="color: #d4af37; font-weight: bold;">PENDING APPROVAL</span></p>
            </div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">Click below to review and manage this user account:</p>

            <div class="btn-container">
                <a href="https://www.mylink.com/admin/users" class="btn">Review User Account</a>
            </div>

            <div class="warning">
                ⚠️ This user account is currently inactive pending administrator approval.
            </div>
        '''
        content = self._inline_styles(content)
        final_content = self.HTML_TEMP.safe_substitute(content=content)
        return final_content

    def reset_password(self, code, email):
        """Password reset email template"""
        safe_email = self.sanitize_input(email)
        safe_code = self.sanitize_input(code)
        
        content = f'''
            <h1 style="color: #d4af37; font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; margin-bottom: 20px; text-align: center;">Password Reset Request</h1>

            <div class="status-indicator">SECURITY VERIFICATION REQUIRED</div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">We received a password reset request for your account: <strong style="color: #d4af37;">{safe_email}</strong></p>

            <div class="message-box">
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 20px; font-size: 15px; text-align: center;">Use the verification code below to reset your password:</p>
                <p style="color: #d4af37; font-family: Arial, sans-serif; font-size: 32px; font-weight: bold; text-align: center; margin: 25px 0; letter-spacing: 4px; background: #f8f9fa; padding: 20px; border-radius: 8px; border: 2px dashed #d4af37;">{safe_code}</p>
                <p style="color: #8b6e1f; font-family: Arial, sans-serif; text-align: center; margin-bottom: 0; font-size: 14px; font-weight: bold;">SECURITY VERIFICATION CODE</p>
            </div>

            <div class="warning">
                ⏰ This code will expire in 30 minutes for security reasons.
            </div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 15px; margin-bottom: 0; line-height: 1.6;">If you didn't request this password reset, please ignore this email or contact support immediately.</p>
        '''
        content = self._inline_styles(content)
        final_content = self.HTML_TEMP.safe_substitute(content=content)
        return final_content

    def approved(self, email):
        """Account approval email template"""
        safe_email = self.sanitize_input(email)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f'''
            <h1 style="color: #d4af37; font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; margin-bottom: 20px; text-align: center;">Account Approved</h1>

            <div class="status-indicator">ACCESS GRANTED</div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">Congratulations! Your SpecterPanel account has been approved and is now active.</p>

            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Account Email</div>
                    <div class="info-value">{safe_email}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Access Level</div>
                    <div class="info-value" style="color: #d4af37;">PREMIUM USER</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Activation Date</div>
                    <div class="info-value">{current_date}</div>
                </div>
            </div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">You now have full access to all SpecterPanel features and can begin using the platform immediately.</p>

            <div class="btn-container">
                <a href="https://www.mylink.com/login" class="btn">Launch Dashboard</a>
            </div>

            <div class="warning">
                🎉 Welcome to SpecterPanel! Start exploring the features available in your dashboard.
            </div>
        '''
        content = self._inline_styles(content)
        final_content = self.HTML_TEMP.safe_substitute(content=content)
        return final_content

    def rejected(self, email):
        """Account rejection email template"""
        safe_email = self.sanitize_input(email)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f'''
            <h1 style="color: #d4af37; font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; margin-bottom: 20px; text-align: center;">Account Application Review</h1>

            <div style="display: inline-block; background-color: rgba(255, 125, 0, 0.1); border: 2px solid #ff7d00; border-radius: 25px; padding: 10px 20px; color: #cc6600; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; margin: 15px 0; text-transform: uppercase; letter-spacing: 0.5px;">
                APPLICATION DENIED
            </div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">Thank you for your interest in SpecterPanel. After careful review, we are unable to approve your account application at this time.</p>

            <div class="message-box">
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 12px; font-size: 15px;"><strong style="color: #d4af37;">Applicant Email:</strong> {safe_email}</p>
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 12px; font-size: 15px;"><strong style="color: #d4af37;">Review Date:</strong> {current_date}</p>
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 0; font-size: 15px;"><strong style="color: #d4af37;">Status:</strong> <span style="color: #ff7d00; font-weight: bold;">NOT APPROVED</span></p>
            </div>

            <div class="warning">
                💡 If you believe this is an error or would like more information, please contact our support team for assistance.
            </div>
        '''
        content = self._inline_styles(content)
        final_content = self.HTML_TEMP.safe_substitute(content=content)
        return final_content

    def target_reached(self, target, ip, operating_system, email):
        """New target registration email template"""
        safe_target = self.sanitize_input(target)
        safe_ip = self.sanitize_input(ip)
        safe_os = self.sanitize_input(operating_system)
        safe_email = self.sanitize_input(email)
        
        content = f'''
            <h1 style="color: #d4af37; font-family: Arial, sans-serif; font-size: 28px; font-weight: bold; margin-bottom: 20px; text-align: center;">New Target Registered</h1>

            <div class="status-indicator">TARGET ACQUISITION</div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">A new target has been successfully registered in your SpecterPanel system.</p>

            <div class="message-box">
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 12px; font-size: 15px;"><strong style="color: #d4af37;">Target Name:</strong> {safe_target}</p>
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 12px; font-size: 15px;"><strong style="color: #d4af37;">IP Address:</strong> {safe_ip}</p>
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 12px; font-size: 15px;"><strong style="color: #d4af37;">Operating System:</strong> {safe_os}</p>
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 12px; font-size: 15px;"><strong style="color: #d4af37;">Registered By:</strong> {safe_email}</p>
                <p style="color: #4a4a4a; font-family: Arial, sans-serif; margin-bottom: 0; font-size: 15px;"><strong style="color: #d4af37;">Registration Time:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>

            <p style="color: #4a4a4a; font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px; line-height: 1.6;">Click below to view and manage this target:</p>

            <div class="btn-container">
                <a href="https://www.mylink.com/targets" class="btn">Manage Targets</a>
            </div>

            <div class="warning">
                📡 Target monitoring is now active. System will track and report target activity.
            </div>
        '''
        content = self._inline_styles(content)
        final_content = self.HTML_TEMP.safe_substitute(content=content)
        return final_content

    # ===== Email Sending Methods =====
    def send_email(self, subject, html_body, recipient):
        """
        Sends email safely with HTML and plain-text fallback.
        """
        try:
            if not self.validate_email(recipient):
                logger.error(f"❌ Invalid email address: {recipient}")
                return False

            msg = EmailMessage()
            # Enhanced plain-text fallback
            plain_text = f"""
            SPECTERPANEL NOTIFICATION
            =========================
            
            Subject: {subject}
            
            This is an important notification from SpecterPanel.
            Please use an HTML-compatible email client to view the full content.
            
            For security reasons, some content may only be visible in HTML format.
            
            © 2024 SpecterPanel Security System
            """
            msg.set_content(plain_text)
            # HTML content
            msg.add_alternative(html_body, subtype="html")

            msg['Subject'] = f"🛡️ {subject}"  # Add shield emoji to subject
            msg['From'] = config.EMAIL
            msg['To'] = recipient

            with smtplib.SMTP(config.SMTP_LINK, config.SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(config.EMAIL, config.EMAIL_PASSWORD)
                smtp.send_message(msg)

            logger.info(f"✅ Email sent successfully to {recipient}")
            return True

        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"❌ Recipient refused: {recipient} - {e}")
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ SMTP authentication failed: {e}")
        except smtplib.SMTPException as e:
            logger.error(f"❌ SMTP error: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected error sending email: {e}")
            logger.error(traceback.format_exc())
        
        return False

    def send_batch_emails(self, subject, html_body, recipients):
        """Send email to multiple recipients"""
        success_count = 0
        failed_count = 0
        
        for recipient in recipients:
            if self.send_email(subject, html_body, recipient):
                success_count += 1
            else:
                failed_count += 1
                
        logger.info(f"📧 Batch email result: {success_count} successful, {failed_count} failed")
        return success_count, failed_count


# ===== Testing =====
if __name__ == "__main__":
    def test_all_templates():
        email_bot = EmailTemplate()
        
        print("🛡️ SpecterPanel Email System - White & Gold Theme")
        print("=" * 50)
        
        # Test SMTP configuration first
        print("🔧 Testing SMTP configuration...")
        if not email_bot.check_smtp_config():
            print("❌ SMTP configuration test failed. Please check your settings.")
            return
        
        test_email = 'omerkemal2023@gmail.com'
        templates_to_test = [
            ('Welcome to SpecterPanel', email_bot.user_notify(test_email)),
            ('New User Registration Alert', email_bot.new_user(test_email)),
            ('Password Reset Request', email_bot.reset_password('SP-789-XYZ', test_email)),
            ('Account Approved', email_bot.approved(test_email)),
            ('Account Application Status', email_bot.rejected(test_email)),
            ('New Target Registration', email_bot.target_reached('Workstation-ALPHA', '192.168.1.100', 'Windows 11 Pro', test_email))
        ]
        
        print("🧪 Testing all email templates...")
        print("-" * 50)
        
        success_count = 0
        for subject, content in templates_to_test:
            print(f"📨 Testing: {subject}")
            if email_bot.send_email(subject, content, test_email):
                print(f"   ✅ {subject} sent successfully")
                success_count += 1
            else:
                print(f"   ❌ {subject} failed to send")
        
        print("-" * 50)
        print(f"🎉 Email testing completed: {success_count}/{len(templates_to_test)} successful")

    # Run comprehensive tests
    test_all_templates()