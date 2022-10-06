from flask import render_template,request
from flask_security import auth_token_required
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
from datetime import datetime,timedelta
from main import celery,app,db
from database import User,tracker
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from celery.schedules import schedule, crontab
from redbeat import RedBeatSchedulerEntry
from weasyprint import HTML,CSS
from httplib2 import Http
import json,smtplib,july,os,redis
import numpy as np


#localhost redis
r=redis.Redis(db=1)
r.flushall()
for i in User.query.all():
    args=[i.id,"Every month"]
    duration=crontab(0,0,day_of_month=1)
    RedBeatSchedulerEntry(f'report-{i.id}', 'application.task.gen_report',duration, args,app=celery).save()
#------functions-----------------

def gchat(webhook,message=None,attach_file=None):
    """Google Chat incoming webhook quickstart."""
    try:
        bot_message = {
            'text': message}
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        response = http_obj.request(
            uri=webhook,
            method='POST',
            headers=message_headers,
            body=json.dumps(bot_message),
        )
        print("gchat sent")
    except Exception as e:
        print(e)


def decode_dict(d):
    result = {}
    for key, value in d.items():
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        if isinstance(value, bytes):
            value = json.loads(value.decode('utf-8'))
        elif isinstance(value, dict):
            value = decode_dict(value)
        result.update({key: value})
    return result

def send_mail(recipient,subject,content="String",message=None,attach_file=None):
    try:
        msg=MIMEMultipart()
        msg["From"]=app.config["SERVER_EMAIL"]
        pwd=app.config["EMAIL_PWD"]
        msg['To']=recipient
        msg['Subject']=subject
        if content=='html':
            msg.attach(MIMEText(message,"html"))
        if attach_file:
            part=MIMEBase("application","octet-stream")
            with open(attach_file,"rb") as attachment:
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
            part.add_header('Content-Disposition',f'attachment;filename="Report.pdf"')
            msg.attach(part)
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(msg["From"], pwd)
        smtp_server.sendmail(msg["From"], recipient, msg.as_string())
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)

def calender(dates,duration,list):
    data = list
    a=july.heatmap(title="Log Activity",dates=dates,
             data=data,cmap="Oranges",
             frame_on=True,month_grid=True,
             horizontal=True,value_label=False,
             date_label=True, weekday_label=True,
             month_label=True,year_label=False,
             colorbar=True,fontfamily="monospace",
             fontsize=16,titlesize="large",
             dpi=200)
    fig=plt.gcf()
    fig.savefig("exported_files/charts/calender.png")
    return


#------------called_routes-----------------
@auth_token_required
@app.route('/gen_report/<int:id>',methods=['GET','POST'])
def report_schedule(id):
    if request.method=="POST":
        data=request.json
        if data and data.get('schedule'):
            if data.get('schedule')=='now':
                gen_report.delay(id)
                return "Sending report...",200
            elif data.get('schedule')=="Every hour":
                duration=crontab(minute='0')
                args=[id,"Every hour"]
            elif data.get('schedule')=="Every day":
                duration=crontab(minute='0',hour='8')
                args=[id,"Every day"]
            elif data.get('schedule')=="Every week":
                duration=crontab(0,0,day_of_week="Monday")
                args=[id,"Every week"]
            elif data.get('schedule')=="Every month":
                args=[id,"Every month"]
                duration=crontab(0,0,day_of_month=1)
            elif data.get('schedule')=="Every year":
                args=[id,"Every year"]
                duration=crontab(0,0,day_of_month=1,month_of_year=1)
            elif data.get('schedule')=="Custom":
                args=[id,"*"]
                duration=crontab(data.get("minute"),
                                data.get("hour"),
                                day_of_month=data.get("day"),
                                month_of_year=data.get("year"))
            else:
                return "Bad Request",400
        else:
            return "Bad Request",400
        entry = RedBeatSchedulerEntry(f'report-{id}', 'application.task.gen_report',duration, args,app=celery)#bug for startswith was for app=celery#
        # entry.save()
    if request.method=="GET":
        try:
            entry=RedBeatSchedulerEntry.from_key(f"redbeat:report-{id}",app=celery)
        except:
            return "not found, create a schedule first",404
    switch=request.args.get("switch")
    if switch=="false":
        entry.enabled=False
    elif switch=="true":
        entry.enabled=True
    entry.save()
    s={"schedule":None}
    k=r.keys(f"redbeat:report-{id}")
    if len(k) > 0:
        s["name"]=entry.name
        s["schedule"]=entry.args[1]
        s["enabled"]=entry.enabled
        s["next"]=entry.next().due_at+timedelta(hours=5,minutes=30)#for ist

        return s,200
    else:
        return "not found, create a schedule first",404

@auth_token_required
@app.route('/alert/<int:tracker_id>',methods=['GET','POST'])
def scheule_alert(tracker_id):
    if request.method=="POST":
        data=request.json
        if data and data.get("schedule"):
            if data.get('schedule')=='now':
                send_alert.delay(tracker_id,data.get("schedule"),data.get("webhook"))
                return "alert sent",200
            elif data.get('schedule')=='Every minute':
                duration=crontab(minute="*")
            elif data.get('schedule')=="Every hour":
                duration=crontab(minute='0',hour='*')
            elif data.get('schedule')=="Every day":
                duration=crontab(minute='0',hour='8')
            elif data.get('schedule')=="Every week":
                duration=crontab(0,0,day_of_week="Monday")
            elif data.get('schedule')=="Every month":
                duration=crontab(0,0,day_of_month=1)
            else:
                return "Bad Request",400
        else:
            return "Bad Request",400
        print(data.get("webhook"))
        entry = RedBeatSchedulerEntry(f'alert-{tracker_id}', 'application.task.send_alert',duration,                 args=[tracker_id,data.get("schedule"),data.get("webhook")],app=celery)
        #bug for startswith was for app=celery#
        # entry.save()
    if request.method=="GET":
        try:
            entry=RedBeatSchedulerEntry.from_key(f"redbeat:alert-{tracker_id}",app=celery)
        except:
            return "not found, create a schedule first",404
    switch=request.args.get("switch")
    print(request.args)
    if switch=="false":
        entry.enabled=False
    elif switch=="true":
        entry.enabled=True
    entry.save()
    k=r.keys(f"redbeat:alert-{tracker_id}")
    print(k)
    s={}
    if len(k) > 0:
        s["name"]=entry.name
        s["args"]=entry.args
        s["enabled"]=entry.enabled
        s["next"]=entry.next().due_at+timedelta(hours=5,minutes=30)#for ist
        return s,200
    else:
        return "not found, create a schedule first",404


#-----------celery_tasks-------------
@celery.task()
def send_alert(tracker_id,s=None,webhook=None):
    t=tracker.query.get(tracker_id)
    if t:
        user=t.parent
    else:
        return "Not found",404

    #-----sending email---
    print(webhook)
    if webhook and webhook!="":
        message=f"""\
Dear {user.username},
Please add a new log to: http://localhost:8080/log/{t.tracker_id}
Tracker name: {t.name}
{t.desc}
        """
        print("sending gchat alert")
        gchat(webhook,message)
    else:
        recipient = user.email
        subject = f'Alert: Add log to {t.name}'
        message=f"""Dear {user.username} you need to add a log to:<br>
        Tracker name: {t.name},<br>
        {t.desc}<br>
        Link:  <a href='http://localhost:8080/log/{t.tracker_id}'>Open in Browser</a>
        """
        print("sending alert email")
        send_mail(recipient,subject,'html',message)
    return "Alert sent",200

@celery.task()
def gen_report(id,s=""):
    user=User.query.filter(User.id==id).first()
    if not user:
        return "user not found"
    if s=="Every hour":
        duration=[datetime.now().replace(minute=0,second=0,microsecond=0),datetime.now().replace(minute=59,second=0,microsecond=0)]
    elif s=="Every week":
        duration=[datetime.now().replace(hour=0,minute=0,second=0,microsecond=0),datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)+timedelta(days=-7)]
    elif s=="Every day":
        duration=[datetime.now().replace(hour=0,minute=0,second=0,microsecond=0),datetime.now().replace(hour=23,minute=59,second=59,microsecond=0)]
    elif s=="Every month" or s=="":
        duration=[]
        duration.append(datetime.now().replace(day=1,hour=0,minute=0,second=0,microsecond=0))
        if duration[0].month == 12:
            duration.append(datetime(duration[0].year, duration[0].month, 31))
        else:
            duration.append(datetime(duration[0].year, duration[0].month + 1, 1) + timedelta(days=-1))
    elif s=="Every year":
        duration=[datetime(year=datetime.now().year-1,month=1,day=1,hour=0,minute=0,second=0,microsecond=0),datetime(year=datetime.now().year-1,month=12,day=31,hour=23,minute=59,second=59,microsecond=0)]

    try:
        dates = july.utils.date_range(duration[0],duration[1])
        log_dict={}
        list=[0]*len(dates)
        for i in user.trackers:
            x,y=[],[]
            fig= plt.figure(figsize=(5,4))
            plt.rcParams['figure.figsize'] = [5,4]
            plt.style.use('seaborn-ticks')
            ax=plt.gca()
            log_dict[i.tracker_id]=[]
            for j in i.logs:
                if (j.log_datetime>duration[0] and j.log_datetime<duration[1]):
                    x.append(j.log_datetime)
                    if i.type=='Integer':
                        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                        plt.ylabel('Int')
                        y.append(int(j.log_value))
                    elif i.type=='Numeric':
                        plt.ylabel('Float')
                        y.append(float(j.log_value))
                    elif i.type=='Multiple-choice':
                        plt.ylabel('Options')
                        y.append(j.log_value)
                    elif i.type=='Time':
                        ax.yaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
                        y.append(datetime.strptime(j.log_value,"%H:%M:%S"))
                    list[j.log_datetime.day-1]+=1
                    log_dict[i.tracker_id].append(j)
            if len(x)>1:
                plt.gcf().autofmt_xdate()
                plt.suptitle("Log trend")
                plt.plot(x,y,marker='o',color='b',linestyle='--')
                plt.margins(0.05)
                fig.savefig(f'exported_files/charts/{i.name}_{i.tracker_id}.svg',bbox_inches ="tight")
            plt.close()

        #----chart creation----
        calender(dates,duration,list)
    except Exception as e:
        print(e)
        return "chart gen error"

    #-------pdf----------
    template=render_template('report.html',user=user,datetime=datetime,log_dict=log_dict)
    htmldoc=HTML(string=template, base_url=os.getcwd())
    css = CSS(string='''* { font-family:'Open Sans';}''')
    htmldoc.write_pdf(f'exported_files/pdf/{user.username}.pdf',stylesheets=[css])
    #-----sending email---
    recipient = user.email
    subject = f'Report'
    body = ''
    email_text = f"""<em>Dear {user.username} your report is ready, download the file from attachment.<em>
    """
    print("sending report email")
    send_mail(recipient,subject,'html',email_text,f'exported_files/pdf/{user.username}.pdf')
    return "Report sent",200
