"# -*- coding: utf-8 -*-"
"""
SpecterPanel - A Flask-based Web Application
This application serves as a web interface for managing and monitoring various tasks.
digits, and lowercase letters.
#         
#         Example:#             >>> ID()
#             'A1b2C'
#         
#         """


from flask import Flask

from utility.setting import Setting
from view.view import view
from view.public import public
from api.api import api
from evet.event import event
#from flaskwebgui import FlaskUI  <-- Change this import

config = Setting()
config.setting_var()

app = Flask(__name__)

app.secret_key = config.SECRAT_KEY

app.register_blueprint(view)
app.register_blueprint(api)
app.register_blueprint(public)
app.register_blueprint(event)

# ui = FlaskUI(app=app, server="flask")


if __name__ == "__main__":
    # Run the Flask application
    # The debug mode is enabled for development purposes
    # In production, it is recommended to set debug=False
    # and use a proper WSGI server like Gunicorn or uWSGI.
    # The application will listen on all interfaces
    # and port 5000 by default.
    # To run the application, execute this script directly.
    # You can also set environment variables to configure the application.
    # For example, you can set FLASK_ENV=development to enable debug mode.
    # The application will automatically reload on code changes
    # when running in debug mode.
    # To access the application, open a web browser and navigate to http://localhost:5000
    # or http://<your-server-ip>:5000 if running on a remote server.
    # Make sure to install the required dependencies
    # by running `pip install -r requirements.txt` before starting the application.
    # This application is designed to be modular and extensible.
    # You can add new features by creating new blueprints
    # and registering them with the Flask application.
    # The application uses Flask's built-in development server,
    # which is suitable for development and testing purposes.
    # For production deployments, consider using a more robust server
    # like Gunicorn or uWSGI, and configure it to serve the application.
    # The application is structured to separate concerns,
    # with views, APIs, and events handled in different modules.
    # This makes it easier to maintain and extend the application.
    # The application is designed to be secure,
    # with a secret key set for session management.
    # Ensure that the secret key is kept confidential
    # and not exposed in version control systems.
    # The application can be customized by modifying the configuration settings
    # in the `utility.setting` module.
    # You can change settings like the secret key,
    # database connection details, and other application-specific configurations.
    # The application is built using Flask, a lightweight WSGI web application framework.
    # Flask is known for its simplicity and flexibility,
    # making it a popular choice for building web applications.
    # The application follows best practices for Flask development,
    # including using blueprints for modularity,
    # separating views, APIs, and events into different modules,
    # and using a configuration file for settings.
    # The application is designed to be easy to deploy and run,
    # with minimal dependencies and a straightforward structure.
    # To run the application, ensure you have Flask installed,
    # and then execute this script. The application will start
    # listening for incoming requests on the specified port.
    # You can access the application through a web browser
    # or use tools like curl `or Postman to interact with the APIs.
    # The application is intended to be a starting point
    # for building more complex web applications.
    app.run(debug=True) # Only call ui.run(), do not call app.run() separately
