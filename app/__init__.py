from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.autodoc import Autodoc

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

# from app.models.{{model_folder}}.model import {{model_name}}
from app.models.user.model import User

db.create_all()
db.session.commit()

from flask.ext.cors import CORS
from app.helpers.DateJSONEncoder import DateJSONEncoder

cors = CORS(app)
app.json_encoder = DateJSONEncoder

auto = Autodoc(app)

#from core.api.users import mod_{{module_name}} as {{module_name}}_module
from app.api.Core import mod_core as core_module

#Charge Module
#core.register_blueprint({{name_module}})
app.register_blueprint(core_module)
