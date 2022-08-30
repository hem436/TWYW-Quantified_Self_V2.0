from flask import redirect, render_template, request
from flask_restful  import Resource,fields,marshal_with,marshal
from flask_security import auth_required,auth_token_required,hash_password,login_user,verify_password,current_user
from database import User,tracker,log,user_datastore,db
import bcrypt
from datetime import datetime
#------------output fields-----------------


tracker_fields={
    "user_id":fields.Integer,
    "tracker_id":fields.Integer,
    "tracker_name":fields.String(attribute='name'),
    "tracker_description":fields.String(attribute='desc'),
    "tracker_type":fields.String(attribute='type'),
    "settings":fields.String,
    "last_updated":fields.String(attribute='lastupdate'),
    "logs":fields.String(attribute=lambda x:[(i.log_id,i.log_value) for i in x.logs])
}
log_fields={
    "tracker_id":fields.Integer,
    "log_id":fields.Integer,
    "log_datetime":fields.String,
    "note":fields.String,
    "log_value":fields.String
}
user_fields={
    "user_id":fields.String(attribute='id'),
    "username":fields.String,
    "trackers":fields.List(fields.Nested(tracker_fields))
}
#------------validation functions----------
def username_valid(name):
    b=(" " not in name)and(name not in [i[0] for i in db.session.query(User.username).all()])
    return b
def password_valid(p):
    b=(" " not in p)
    return b
def tracker_name_valid(tname):
    b= type(tname) is str
    return b
def tracker_type_valid(ttype):
    b= ttype in ("Integer","Numeric","Multiple-choice","Time")
    return b


#---------API-----------
class LoginApi(Resource):
    def get(self):
        pass
    def post(self):
        try:
            loginuser=request.json
            print(loginuser)
            username=loginuser["username"]
            pwd=loginuser["password"]
            user_valid=username and username.isalnum()
            pass_valid=pwd and password_valid(pwd)
            if user_valid and pass_valid:
                if (username,) in db.session.query(User.username).all():
                    dbuser=User.query.filter(User.username==username).first()
                    if verify_password(pwd,dbuser.password):
                        print(login_user(dbuser,remember=True,authn_via=["password"]))
                        return {**marshal(dbuser,user_fields),
                        "auth_token":dbuser.get_auth_token()},200
                    else:
                        print("invalid_password")
                else:
                    print("user not found")
        except Exception as e:
            print(e)

class UserApi(Resource):
    @auth_token_required
    def get(self,username):
        try:
            if username=="*":
                user=User.query.all()
            elif " " not in username:
                user=User.query.filter(User.username==username).first()
            else:
                return "invalid user",400
            #print(user) #debug print
            if user != None:
                # print({*user,user.get_auth_token()})
                return marshal(user,user_fields),200
            else:
                return "User not found",404
        except:
            return "Internal Server Error",500

    @auth_token_required
    def put(self,username):
        try:
            newdata=request.json
            q=User.query.filter(User.username==username)
            pdata=q.one()
            if pdata==None:
                return "User not found",404
            modified_username=newdata["modified_username"]
            modified_password=newdata["modified_password"]
            b1=(pdata.username!=modified_username)
            b2=(pdata.password!=modified_password)
            if  b1 or b2:
                uname_valid=username_valid(modified_username)
                pass_valid=password_valid(modified_password)
                if uname_valid and pass_valid:
                    q.update({"username":str(modified_username),
                    "password":str(modified_password)})
                    db.session.commit()
                elif not uname_valid:
                    return "Modified Username is invalid",400
                elif not pass_valid:
                    return "Modified Password is invalid",400
            return self.get(modified_username)
        except:
            return "Internal Server Error",500

    @auth_token_required
    def delete(self,username):
        try:
            user=User.query.filter(User.username==username).first()
            if user==None:
                return "User not found",404
            else:
                db.session.delete(user)
                db.session.commit()
            return "OK",200
        except:
            return "Internal Server Error",500

    def post(self):
        try:
            data=request.json
            if data:
                if username_valid(data['username']) and password_valid(data['password']):
                    # db.session.add(new_user)
                    user_datastore.create_user(username=str(data['username']),
                    email=str(data['username'])+"@gmail.com",password=hash_password(data['password']))
                    dbuser=user_datastore.find_user(username=str(data['username']))
                    login_user(dbuser)
                    db.session.commit()
                elif not username_valid(data['username']):
                    return "Username is invalid",400
                elif not password_valid(data['password']):
                    return "Password is invalid",400
            return {**marshal(dbuser,user_fields),"auth_token":dbuser.get_auth_token()},200
        except Exception as e:
            return "Internal Server Error",500

class TrackerApi(Resource):

    @auth_token_required
    def get(self,tracker_id):
        try:
            trk=tracker.query.get(int(tracker_id))
            if trk==None:
                return "Tracker id not found",404
            if trk.user_id!=current_user.id:
                return "not authorized to access this tracker",400
            return {**marshal(trk,tracker_fields),"log_objects":marshal(trk.logs,log_fields)}
        except:
            return "Internal Server Error",500

    @auth_token_required
    def post(self):
        try:
            tdata=request.json
            uid=tdata["user_id"]
            tname=tdata["tracker_name"]
            tdesc=tdata["tracker_description"]
            ttype=tdata["tracker_type"]
            tset=tdata["settings"]
            tnv=tracker_name_valid(tname)
            ttv=tracker_type_valid(ttype)
            if uid!=current_user.id:
                return "Not authorized to add tracker to this user",400
            if ttype!="Multiple-choice":
                tset=""
            elif tset=="":
                return "tracker options cannot be null for multiple choice",400
            if not tnv:
                return "tracker name not valid",400
            elif not ttv:
                return "tracker type not valid",400
            tobj=tracker(user_id=int(uid),name=str(tname),desc=str(tdesc),
            type=str(ttype),settings=str(tset))
            db.session.add(tobj)
            db.session.commit()
            return marshal(tobj,tracker_fields),200
        except:
            return "Internal Server Error",500

    @auth_token_required
    def put(self,tracker_id):
        try:
            pdata=request.json
            tname=pdata["modified_tracker_name"]
            ttype=pdata["tracker_type"]
            tset=pdata["modified_tracker_settings"]
            q=db.session.query(tracker).filter(tracker.tracker_id==tracker_id)
            if q.first().user_id!=current_user.id:
                return "Not authorized to access this tracker",400
            if q.first()==None:
                return "Tracker id not found",404
            if ttype!=q.first().type:
                return "Tracker type cannot be changed",400
            if ttype!="Multiple-choice":
                    tset=""
            update_dict={"name":tname,
            "desc":pdata["modified_tracker_description"],
            "settings":tset,
            }
            if not tracker_name_valid(tname):
                return "name not valid",400
            elif not tracker_type_valid(ttype):
                return "tracker type not valid",400
            q.update(update_dict)
            db.session.commit()
            return marshal(q.first(),tracker_fields),200
        except Exception as e:
            print(e)
            return "Internal Server Error",500


    @auth_token_required
    def delete(self,tracker_id):
        tobj=tracker.query.get(int(tracker_id))
        if tobj.user_id!=current_user.id:
            return "Not authorized to access this tracker",400
        tlogs=log.query.filter(log.tracker_id==tracker_id).all()
        db.session.delete(tobj)
        db.session.commit()
        return "OK",200

class LogApi(Resource):
    @auth_token_required
    def get(self,log_id):
        try:
            logobj=log.query.get(int(log_id))
            if logobj.parent.user_id!=current_user.id:
                return "Not authorized to access this log",400
            if logobj:
                return marshal(logobj,log_fields)
            else:
                return "NOT FOUND",404
        except:
            return "INTERNAL SERVER ERROR",500

    @auth_token_required
    def put(self,log_id):
        try:
            if (log_id,) not in db.session.query(log.log_id).all():
                return 'log_id_not_found',400
            l=log.query.get(int(log_id))
            t=l.parent
            if t.user_id!=current_user.id:
                return "Not authorized to access this log",400
            ldata=request.json
            lval=ldata['log_value']
            lnote=ldata['log_note']
            ldatetime=datetime.strptime(ldata['log_datetime'],'%d/%b/%Y, %H:%M:%S.%f')
            if t.lastupdate==None or t.lastupdate<ldatetime:
              t.lastupdate=ldatetime
            db.session.query(log).filter(log.log_id==log_id).update({'log_value':lval,
            'note':lnote,'log_datetime':ldatetime})
            db.session.commit()
            return "OK",200
        except Exception as e:
            print(e)
            return "Internal Server Error",500
    @auth_token_required
    def delete(self,log_id):
        try:
            l=log.query.get(int(log_id))
            if l:
                t=l.parent
                if t.user_id!=current_user.id:
                    return "Not authorized to access this log",400
                db.session.delete(l)
                if t.lastupdate==l.log_datetime:
                  lastlog=log.query.filter(log.tracker_id==t.tracker_id).order_by(log.log_datetime.desc()).first()
                  if lastlog:
                    t.lastupdate=lastlog.log_datetime
                  else:
                    t.lastupdate=None
                db.session.commit()
                return "OK",200
            else:
                return "NOT FOUND",404
        except Exception as e:
            print(e)
            return "INTERNAL SERVER ERROR",500

    @auth_token_required
    def post(self):
        try:
            ldata=request.json
            ltid=ldata["tracker_id"]
            lval=ldata['log_value']
            lnote=ldata['log_note']
            ldatetime=datetime.strptime(ldata['log_datetime'],'%d/%b/%Y, %H:%M:%S.%f')
            #Validation
            #----------
            t=tracker.query.get(ltid);
            if t.user_id!=current_user.id:
                return "Not authorized to add log to this tracker",400
            if t.lastupdate==None or t.lastupdate<ldatetime:
                t.lastupdate=ldatetime
            lobj=log(tracker_id=ltid,log_datetime=ldatetime,note=lnote,log_value=lval)
            db.session.add(lobj)
            db.session.commit()
            return "OK",200
        except Exception as e:
            print(e)
            return "INTERNAL SERVER ERROR ",500

#===========Api===========
