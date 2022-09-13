# -*- coding: utf-8 -*-
#basic imports
from datetime import datetime
import os,csv
from flask import Flask, flash, redirect, render_template, request
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
# from matplotlib import pyplot as plt
# from matplotlib.dates import DateFormatter
# from matplotlib.ticker import MaxNLocator
#------------imports in version 2----------
from application.config import LocalDevelopmentConfig
from application import worker
from flask_security import login_required,login_user,logout_user,auth_required,current_user
from flask_security import Security,SQLAlchemyUserDatastore,hash_password,verify_password
from flask_cors import CORS
from database import *
app=None
api=None
celery=None
def create_app():
    #app initialization
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    app.app_context().push()
    #celery init
    celery=worker.celery
    celery.conf.update(
    broker_url=app.config["CELERY_BROKER_URL"],
    redbeat_redis_url = app.config["CELERY_BROKER_URL"],
    result_backend=app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = worker.ContextTask
    app.app_context().push()
    #Api section----------------#
    api= Api(app)
    app.app_context().push()
    #login init
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.app_context().push()
    #database init
    db.init_app(app)
    app.app_context().push()
    #security init
    security = Security(app, user_datastore)
    CORS(app);
    app.app_context().push()
    return app,api,celery,db
app,api,celery,db=create_app()

#api controllers imports
from application.api import *
api.add_resource(UserApi,'/api/user/<string:username>','/api/user')
api.add_resource(TrackerApi,'/api/tracker/<int:tracker_id>','/api/tracker')
api.add_resource(LoginApi,'/api/login')
api.add_resource(LogApi,'/api/log/<int:log_id>','/api/log')

from application.controllers import *

#====================================================================================
#app run
if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
