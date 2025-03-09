class email_temp:
    def __init__(self):
        self.HTML_TEMP = '''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>New User Registration</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        background: #ffffff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    }}
                    h1 {{
                        color: #333;
                    }}
                    p {{
                        font-size: 16px;
                        color: #555;
                    }}
                    .btn {{
                        display: inline-block;
                        padding: 12px 25px;
                        margin-top: 15px;
                        background-color: #007bff;
                        color: #ffffff;
                        text-decoration: none;
                        border-radius: 5px;
                        font-size: 16px;
                        font-weight: bold;
                    }}
                    .btn:hover {{
                        background-color: #0056b3;
                    }}
                    .footer {{
                        margin-top: 20px;
                        font-size: 14px;
                        color: #888;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    {}
                </div>
            </body>
        </html>
        '''

    def new_user(self, email):
        body = f'''
            <h1>New User Registration Alert</h1>
            <p>Dear Administrator,</p>
            <p>A new user has just registered on your platform. Below are the details:</p>
            <p><strong>Email:</strong> {email}</p>
            <p>Please review this registration and take any necessary actions if required.</p>
            <a href="https://www.mylink.com/users" class="btn">View User Details</a>
            <p class="footer">This is an automated notification. If you have any concerns, please contact support.</p>
        '''
        return self.HTML_TEMP.format(body)

    def reset_password(self, code):
        body = f'''
        <h1>Password Reset Request</h1>
        <p>Hello,</p>
        <p>We received a request to reset your password. If you did not make this request, you can ignore this email.</p>
        <p>To reset your password, please use this code below:</p>
        <p><strong>{code}</strong></p>
        <p class="footer">This code will expire in 30 minutes for security reasons.</p>
        <p class="footer">If you need further assistance, please contact support.</p>
        '''
        return self.HTML_TEMP.format(body)

    def approved(self):
        body = '''
        <h1>Congratulations! Your Account Has Been Approved</h1>
        <p>Hello,</p>
        <p>We are pleased to inform you that your account has been successfully approved by our team. You can now log in and start using our platform.</p>
        <p>Click the button below to access your account:</p>
        <a href="https://www.mylink.com/login" class="btn">Login to Your Account</a>
        <p>If you have any questions or need further assistance, feel free to contact our support team.</p>
        <p class="footer">Thank you for being a part of our community!</p>
        '''
        return self.HTML_TEMP.format(body)

    def rejected(self):
        body = '''
        <h1>We Regret to Inform You That Your Account Has Been Rejected</h1>
        <p>Hello,</p>
        <p>We regret to inform you that your account registration has been rejected by our team. If you have any questions or need further clarification, please contact our support team.</p>
        '''
        return self.HTML_TEMP.format(body)

