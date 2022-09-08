from flask import redirect, render_template,send_from_directory,request,url_for
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
# from matplotlib import cm
from main import celery,current_user,datetime,app,db
from database import User,tracker,log,user_datastore
import numpy as np
import csv,time,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from celery.schedules import crontab
from weasyprint import HTML,CSS
from pathlib import Path
import base64,smtplib,july


# @celery.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, print_current_time_job.s(), name='add every 10')
#------functions-----------------
def send_mail(server_user,pwd,recipient,subject,content,message,attach_file):
    try:
        msg=MIMEMultipart()
        msg["From"]=server_user
        msg['To']=recipient
        msg['Subject']=subject
        if content=='html':
            msg.attach(MIMEText(message))
        if attach_file:
            part=MIMEBase("application","octet-stream")
            with open(attach_file,"rb") as attachment:
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
            part.add_header('Content-Disposition',f'attachment;filename={attach_file}')
            msg.attach(part)
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(server_user, pwd)
        smtp_server.sendmail(server_user, recipient, msg.as_string())
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)

def calender(duration):
    dates = july.utils.date_range(duration[0],duration[1])
    data = np.random.randint(0, 14, len(dates))
    a=july.heatmap(dates=dates,
             data=data,
             cmap="Oranges",
             month_grid=True,
             horizontal=True,
             value_label=False,
             date_label=False,
             weekday_label=True,
             month_label=True,
             year_label=True,
             colorbar=False,
             fontfamily="monospace",
             fontsize=10,
             titlesize="large",
             dpi=200)
    # a=july.calendar_plot(dates, data,
    #         cmap="Oranges",
    #          value_label=False,
    #          date_label=False,
    #          month_label=True,
    #          fontfamily="monospace",
    #          fontsize=12,
    #          title=True,
    #          dpi=100)
    # fig.colorbar(cm.ScalarMappable(cmap='Oranges'))
    fig = plt.gcf()

    fig.savefig("exported_files/calender.png")


#------------called_routes-----------------

@app.route('/gen_report',methods=['GET','POST'])
def hello():
    if request.method=='POST':
        duration=request.json['duration']
    job=gen_report.delay(current_user.id,duration)
    return "report generating...",200


@app.route('/schedule/alert/<int:tid>',methods=['GET','POST'])
def scheuling(tid):
    msg=""
    if request.method=='POST':
        t=tracker.query.get(tracker_id)
        data=request.json
        print(data)


#-----------celery_tasks-------------
@celery.task()
def just_say_hello(name):
     print("inside celery task")
     print(app,db)
     return f'hello {name}'


@celery.task()
def print_current_time_job():
     print("START")
     now = datetime.now()
     print("now =", now)
     dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
     print("date and time =", dt_string)
     print("COMPLETE")

@celery.task()
def export_tracker(id):
    p=os.path
    user=User.query.filter(User.id==id).first()
    if not user:
        return "User not found"
    filename=f'{user.username}.csv'
    filepath=p.normpath(p.join(p.dirname(__file__),
    f'../static/exported_files/{filename}'))
    file=open(filepath,'w',newline='', encoding='utf-8')
    w=csv.writer(file,lineterminator='\n')
    user_header=['User_id','User_name','Email','Number_of_trackers']
    tracker_header=['S.N','Last_updated','Tracker_id','Tracker_name','Tracker_description','Tracker_type',"Tracker_settings"]
    w.writerow([user.id,user.username,user.email,len(user.trackers)])
    w.writerow([Trackers])
    w.writerow(tracker_header)
    i=0
    for t in user.trackers:
        i+=1
        w.writerow([i,t.lastupdate,t.tracker_id,t.name,t.desc,t.type,t.settings])
    file.close()
    time.sleep(2)
    # send_from_directory(filepath,filename)
    return filepath

@celery.task()
def gen_report(id,duration=""):
    user=User.query.filter(User.id==id).first()
    if not user:
        return "user not found"
    arg={}
    arg['duration']=duration
    with open("./static/userimg.png", "rb") as image_file:
        arg["userimg"] = base64.b64encode(image_file.read()).decode('utf-8')
    #-------pdf----------
    template=render_template('report.html',user=user,datetime=datetime,arg=arg)
    # htmldoc=HTML(string=template, base_url=os.getcwd())
    # css = CSS(string='''* { font-family:'Open Sans';}''')
    # htmldoc.write_pdf('out.pdf',stylesheets=[css])
    #-----sending email---
    server_user = "hemantnohack@gmail.com" ####
    pwd = "acrugxtlyiqkkvje"                ##
    recipient = 'hemant436268s@gmail.com'
    subject = f'Report {duration} '
    body = ''
    email_text = f"""Dear {user.username} your report is ready, download the file from attachment.
    """

    send_mail(server_user,pwd,recipient,subject,'html',email_text,f'exported_files/pdf/{user.username}.pdf')
    return "template"
    #

calender(["2020-01-20", "2020-12-31"])
