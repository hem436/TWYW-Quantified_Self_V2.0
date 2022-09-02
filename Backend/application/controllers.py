import os,csv
from flask import redirect, render_template, request
from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator
from database import User,tracker,log,user_datastore,db
#==============================Business Logic====================================
#------------Login-Logout-------------
from main import app
from datetime import datetime
from flask_security import hash_password,verify_password,login_user,login_required,current_user
from application import task

login_manager=app.login_manager
@login_manager.user_loader
def load_user(id):
    u=User.query.filter(User.fs_uniquifier==id).one()
    # print("user in load user=",u)
    return u

@app.route('/hello')
def hello():
    with app.app_context():
        job=task.just_say_hello.delay("hemant")
    # job2=task.export_tracker.delay(current_user.id)
    # job3=task.gen_report.delay(current_user.id)
    return str(job.wait()),200

#-------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        uname=request.form.get('username')
        passd=request.form.get('password')
        try:

            user=User.query.filter(User.username==uname).one()
            print(verify_password(passd,user.password))
        except Exception as e:
            print(e)
            return render_template('login.html',error='incorrect password or username')
        if not current_user.is_authenticated:
            print(login_user(user,remember=True,authn_via=["password"]))
    if current_user.is_authenticated:
        return main()
    else:
        return render_template('login.html')
#---------------------------
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        uname=request.form.get('username')
        passd=request.form.get('password')
        email=request.form.get('email')
        if uname not in [i.username for i in User.query.all()]:
            # user=User(username=uname,password=passd,fs_uniquifier=bcrypt.gensalt())
            user_datastore.create_user(username=uname,email=email, password=hash_password(passd))
            # db.session.add(user)
            db.session.commit()
            return login()
        return redirect('/notfound/User already exists.')
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return login()
#---------------------Not found error ----------------
@app.route("/notfound/<error>")
def notfound(error):
    return render_template('notfound.html',error=error)

#-------------------Tracker---------------------------
@app.route('/main')
@login_required
def main():
    return render_template('main.html',user=current_user,datetime=datetime)

@app.route('/tracker/add',methods=['GET','POST'])
@login_required
def add_tracker():
    if request.method=='POST':
        try:
            u_id=current_user.id
            # print(u_id)
            name=request.form.get('name')
            desc=request.form.get('desc')
            type=request.form.get('type')
            set=request.form.get('settings')
            #---validation----
            if name in [i.name for i in User.query.get(u_id).trackers]:
                return notfound('Tracker name should be unique')

            if type=='Multiple-choice':
                if set=="":
                    return notfound('Tracker setting not valid, Multi-Choice should have setting separated by comma.')
            elif set!="":
                set=""
            #-----------------
            add=tracker(user_id=u_id,name=name,desc=desc,type=type,settings=set)
            db.session.add(add)
            db.session.commit()
            return main()
        except Exception as e:
            db.session.rollback()
            return(f'-------add_tracker_db_error-------{e}')
    return render_template('add_tracker.html',user=current_user)

@app.route('/tracker/<int:tracker_id>',methods=['GET','POST'])
@login_required
def view_tl(tracker_id):
  try:
        #Validarion
        if (tracker_id,) not in db.session.query(tracker.tracker_id).all():
            return notfound('tracker_id_not_found')
        t=tracker.query.get(tracker_id)
        tl=log.query.filter(log.tracker_id==tracker_id).order_by(log.log_datetime)
        #---------------
        x,y,file,filename=[],[],None,None
        fig=plt.figure(figsize=(8,5))
        ax = fig.gca()
        if request.method=='POST' and request.form.get('period'):
            p=request.form.get('period')
            if p=='Custom':
                llim=request.form['customdatetimel']
                hlim=request.form['customdatetimeh']
                comp='%Y-%m-%dT%H:%M'
            elif p=='Today':
                llim=datetime.today().strftime('%d/%m/%y')
                hlim=llim
                comp='%d/%m/%y'
            elif p=='1Month':
                llim=datetime.today().strftime('%m/%y')
                hlim=llim
                comp='%m/%y'
            elif p=='All':
                llim,hlim,comp='','',''
            if request.form.get('button')=="export_data":
                filename=request.form.get("filename")

                file=open(f'static/exported_files/{filename}.csv','w')
                w=csv.writer(file)
        else:
          llim,hlim,comp='','',''

        for i in tl:
            if i.log_datetime.strftime(comp)>=llim and i.log_datetime.strftime(comp)<=hlim:
                x.append(i.log_datetime)
                if t.type=='Integer':
                    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                    plt.ylabel('Int')
                    y.append(int(i.log_value))
                elif t.type=='Numeric':
                    plt.ylabel('Float')
                    y.append(float(i.log_value))
                elif t.type=='Multiple-choice':
                    plt.ylabel('Options')
                    y.append(i.log_value)
                elif t.type=='Time':
                    ax.yaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
                    y.append(datetime.strptime(i.log_value,"%H:%M:%S"))
        plt.plot(x,y,marker='o',color='b',linestyle='--')
        plt.gcf().autofmt_xdate()
        plt.savefig('static/chart.png')
        if file:
            w.writerow(['Timestamp','Log_value'])
            for i in range(len(x)):
                w.writerow((x[i],y[i]))
            file.close()
        if len(x)>0:

            img='/static/chart.png'
        else:
            img=""
        return render_template('tracker.html',tracker=t,chart=img,filename=filename)
  except Exception as e:
      print(e)
      return(main())


@app.route('/tracker/<int:tracker_id>/update',methods=['GET','POST'])
@login_required#*************************
def update_tracker(tracker_id):
    #Validarion
    if (tracker_id,) not in db.session.query(tracker.tracker_id).all():
        return notfound('tracker_id_not_found')
    t=tracker.query.get(tracker_id)
    if request.method=='POST':
        try:
            if request.form.get('type')!=t.type or request.form.get('settings')!=t.settings:
                db.session.query(log).filter(log.tracker_id==tracker_id).delete()
            updict={tracker.name:request.form['name'],tracker.desc:request.form['desc'],tracker.type:request.form['type'],tracker.settings:request.form['settings']}
            db.session.query(tracker).filter(tracker.tracker_id==tracker_id).update(updict)
            db.session.commit()
            return main()
        except:
            print('-------------db_update_error--------------')
            db.session.rollback()

    return render_template('update_tracker.html',tracker=t,user=current_user)

@app.route('/tracker/<int:tracker_id>/delete',methods=['GET','POST'])
@login_required
def delete_tracker(tracker_id):
    #Validarion
    if (tracker_id,) not in db.session.query(tracker.tracker_id).all():
        return notfound('tracker_id_not_found')
    t=tracker.query.get(tracker_id)
    try:
        db.session.delete(t)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print('----tracker_delete_dberror------',e)
    return main()
#-----------------------------logs---------------------------
@app.route('/<int:tracker_id>/log/add',methods=['GET','POST','PUT'])
@login_required
def add_logs(tracker_id): #
    #Validation
    if (tracker_id,) not in db.session.query(tracker.tracker_id).all():
        return notfound('tracker_id_not_found')
    t=tracker.query.get(tracker_id)
    #EndV
    if request.method=='POST':
        try:
            value=request.form.get('value')
            if t.type=='Time':
              check=datetime.strptime(value,'%H:%M:%S')
            log_datetime=datetime.strptime(request.form.get("time"),'%d/%b/%Y, %H:%M:%S.%f')
            if t.lastupdate==None or t.lastupdate<log_datetime:
                t.lastupdate=log_datetime
            l=log(tracker_id=tracker_id,log_datetime=log_datetime,note=request.form.get('note'),log_value=value)
            db.session.add(l)
            db.session.commit()
            return view_tl(tracker_id)
        except:
            db.session.rollback()
            print('-------------db_log_add_error--------------')
    timedict={'start':'','end':'','duration':''}
    if request.method=='GET':
        if request.args.get('start'):
            s=request.args.get('start')
        elif request.args.get('startb')=="start":
            s=datetime.now().strftime('%H:%M:%S')
        else:
            s=''
        if request.args.get('end'):
            e=request.args.get('end')
        elif request.args.get('endb')=="end":
            e=datetime.now().strftime('%H:%M:%S')
        else:
            e=''
        d=''
        if s!='' and e!='':
            d=datetime.strptime(e,'%H:%M:%S')-datetime.strptime(s,'%H:%M:%S')
        timedict={'start':s,'end':e,'duration':d}
    return render_template('add_logs.html',t=t,datetime=datetime,timedict=timedict)

@app.route('/<int:log_id>/log/update',methods=['GET','POST'])
@login_required
def update_log(log_id):#############more validation needed#######
    #validation
    if (log_id,) not in db.session.query(log.log_id).all():
        return notfound('log_id_not_found')
    l=log.query.get(log_id)
    t=l.parent
    #EndV
    if request.method=='POST':
        log_value=request.form.get("value")#
        log_note=request.form.get("note")
        log_datetime=datetime.strptime(request.form.get("time"),'%d/%b/%Y, %H:%M:%S.%f')
        if t.lastupdate==None or t.lastupdate<log_datetime:
          t.lastupdate=log_datetime
        db.session.query(log).filter(log.log_id==log_id).update({'log_value':log_value,'note':log_note,'log_datetime':log_datetime})
        db.session.commit()
        return view_tl(l.tracker_id)
    return render_template('update_logs.html',datetime=datetime,log=l)

@app.route('/<int:log_id>/log/delete',methods=['GET','POST'])
@login_required
def delete_log(log_id):
    #validation
    if (log_id,) not in db.session.query(log.log_id).all():
        return notfound('log_id_not_found')
    l=log.query.get(log_id)
    t=l.parent
    db.session.delete(l)
    if t.lastupdate==l.log_datetime:
      lastlog=log.query.filter(log.tracker_id==t.tracker_id).order_by(log.log_datetime.desc()).first()
      if lastlog:
        t.lastupdate=lastlog.log_datetime
      else:
        t.lastupdate=None
    db.session.commit()
    return view_tl(t.tracker_id)
