import os
from flask import redirect, render_template,send_from_directory,request,current_app as app
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
from main import login_manager,login_required,current_user,datetime
from database import User,tracker,log,user_datastore,db
import numpy as np
import csv
from application.worker import celery
from celery.schedules import crontab

# @celery.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, print_current_time_job.s(), name='add every 10')

@celery.task()
def just_say_hello(name):
     print("inside celery task")
     print(f'hello {name}')


@celery.task()
def print_current_time_job():
     print("START")
     now = datetime.now()
     print("now =", now)
     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
     print("date and time =", dt_string)
     print("COMPLETE")

# @celery.task()
def export_tracker():
    p=os.path
    user=current_user
    if not user:
        return
    filename=f'{user.username}.csv'
    filepath=p.normpath(p.join(p.dirname(__file__),
    f'../static/exported_files/{filename}'))

    file=open(filepath,'w',newline='', encoding='utf-8')
    w=csv.writer(file,lineterminator='\n')
    user_header=['User_id','User_name','Email','Number_of_trackers']
    tracker_header=['S.N','Last_updated','Tracker_id','Tracker_name','Tracker_description','Tracker_type',"Tracker_settings"]
    w.writerow(user_header)
    w.writerow([user.id,user.username,user.email,len(user.trackers)])
    w.writerow([])
    w.writerow(tracker_header)
    i=0
    for t in user.trackers:
        i+=1
        w.writerow([i,t.lastupdate,t.tracker_id,t.name,t.desc,t.type,t.settings])
    file.close()
    send_from_directory(filepath,filename)
    return True
