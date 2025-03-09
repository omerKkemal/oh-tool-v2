from flask import Flask

from utility.setting import Setting
from view.view import view
from homePage.public import public
from api.api import api

config = Setting()
config.setting_var()

app = Flask(__name__)

app.secret_key = config.SECRAT_KEY

app.register_blueprint(view)
app.register_blueprint(api)
app.register_blueprint(public)


if __name__ == "__main__":
    app.run(debug=True)
