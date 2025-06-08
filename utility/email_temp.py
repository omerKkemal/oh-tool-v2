class email_temp:
    """
    Provides HTML email templates for various SpecterPanel system notifications.
    """

    def init(self):
        """
        Initializes the base HTML template used for all emails.
        """
        self.HTML_TEMP = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>SpecterPanel Notification</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: #0d1117;
                    font-family: 'Segoe UI', sans-serif;
                    color: #f0f6fc;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    padding: 30px;
                    background-color: #161b22;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 255, 255, 0.05);
                    text-align: left;
                }}
                h1 {{
                    color: #58a6ff;
                    font-size: 22px;
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 15px;
                    color: #c9d1d9;
                }}
                a.btn {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 12px 24px;
                    font-weight: bold;
                    text-decoration: none;
                    background-color: #00ffd5;
                    color: #0d1117;
                    border-radius: 5px;
                }}
                a.btn:hover {{
                    background-color: #00ccaa;
                }}
                .footer {{
                    font-size: 13px;
                    color: #8b949e;
                    margin-top: 30px;
                    border-top: 1px solid #30363d;
                    padding-top: 15px;
                    text-align: center;
                }}
                .highlight {{
                    font-weight: bold;
                    color: #00ffd5;
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
        """
        Generates an email template for notifying about a new user registration.

        Args:
            email (str): The email address of the new user.

        Returns:
            str: HTML content for the new user notification email.
        """
        body = f'''
        <h1>New Agent Registration</h1>
        <p>Dear Operator,</p>
        <p>A new user has registered to your SpecterPanel system.</p>
        <p><span class="highlight">Email:</span> {email}</p>
        <p>Click below to review or approve the user:</p>
        <a href="https://www.mylink.com/users" class="btn">Manage Users</a>
        <div class="footer">SpecterPanel • Secure C2 Interface</div>
        '''
        return self.HTML_TEMP.format(body)

    def reset_password(self, code):
        """
        Generates an email template for password reset requests.

        Args:
            code (str): The password reset code.

        Returns:
            str: HTML content for the password reset email.
        """
        body = f'''
        <h1>Password Reset Requested</h1>
        <p>We received a request to reset your password.</p>
        <p>Use the code below to continue:</p>
        <p style="font-size: 20px; font-weight: bold; color: #00ffd5;">{code}</p>
        <p>This code will expire in 30 minutes.</p>
        <div class="footer">If you did not request this, ignore it. SpecterPanel Security</div>
        '''
        return self.HTML_TEMP.format(body)

    def approved(self):
        """
        Generates an email template for notifying users that their account has been approved.

        Returns:
            str: HTML content for the approval notification email.
        """
        body = '''
        <h1>Access Approved</h1>
        <p>Congratulations, your SpecterPanel account has been approved.</p>
        <p>You may now access the dashboard and begin operations.</p>
        <a href="https://www.mylink.com/login" class="btn">Login Now</a>
        <div class="footer">SpecterPanel • Control. Execute. Disappear.</div>
        '''
        return self.HTML_TEMP.format(body)

    def rejected(self):
        """
        Generates an email template for notifying users that their account request was rejected.

        Returns:
            str: HTML content for the rejection notification email.
        """
        body = '''
        <h1>Access Denied</h1>
        <p>Your SpecterPanel account request has been rejected by the system administrator.</p>
        <p>If you believe this is an error, please contact the support team.</p>
        <div class="footer">SpecterPanel • Silent by Design</div>
        '''
        return self.HTML_TEMP.format(body)