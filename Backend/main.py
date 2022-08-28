# -*- coding: utf-8 -*-
#basic imports
import csv
from datetime import datetime
import os
import bcrypt
from flask import Flask, flash, redirect, render_template, request
from flask_login import LoginManager
from flask_security import login_required,login_user,current_user,logout_user,auth_required
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
#V2IMPORTS
from application.config import LocalDevelopmentConfig
from application.worker import *
from flask_security import Security,SQLAlchemyUserDatastore,hash_password,verify_password
from flask_cors import CORS

#app initialization
app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)




celery.conf.update(
broker_url=app.config["CELERY_BROKER_URL"],
result_backend=app.config["CELERY_RESULT_BACKEND"]
)
celery.Task = ContextTask
app.app_context().push()

api= Api(app)
app.app_context().push()
#Api section----------------#
from application.api import *
api.add_resource(UserApi,'/api/user/<string:username>','/api/user')
api.add_resource(TrackerApi,'/api/tracker/<int:tracker_id>','/api/tracker')
api.add_resource(LoginApi,'/api/login')
api.add_resource(LogApi,'/api/log/<int:log_id>','/api/log')

#database import
from database import *
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
security = Security(app, user_datastore)
CORS(app);

#controllers imports
from application.controllers import *

#====================================================================================
#app run
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
