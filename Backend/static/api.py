from flask import redirect, render_template, request
from flask_restful  import Resource,fields,marshal_with,marshal
from flask_login import login_required
from database import User,tracker,log,db
import bcrypt
#------------output fields-----------------
user_fields={
    "user_id":fields.String(attribute='id'),
    "username":fields.String,
    "trackers":fields.String(attribute=lambda x: [(i.tracker_id,i.name) for i in x.trackers])
}
tracker_fields={
    "user_id":fields.Integer,
    "tracker_id":fields.Integer,
    "tracker_name":fields.String(attribute='name'),
    "tracker_description":fields.String(attribute='desc'),
    "tracker_type":fields.String(attribute='type'),
    "settings":fields.String,
    "last updated":fields.String(attribute='lastupdate'),
    "logs":fields.String(attribute=lambda x:[(i.log_id,i.log_value) for i in x.logs])
}
#------------validation functions----------
def username_valid(name):
    b=(" " not in name)and(name not in [i[0] for i in db.session.query(User.username).all()])
    return b
def password_valid(p):
    b=(" " not in p)
    return b
def tracker_name_valid(tname):
    b=(" " not in tname)
    return b
def tracker_type_valid(ttype):
    b= ttype in ("Integer","Numeric","Multi-choice","Time")
    return b
#---------API-----------
class UserApi(Resource):

    def get(self,username):
        try:
            if username=="*":
                user=User.query.all()
            elif " " not in username:
                user=User.query.filter(User.username==username).all()
            else:
                user=[]
            #print(user) #debug print
            if user != []:
                return [marshal(i,user_fields) for i in user]
            else:
                return "User not found",404
        except:
            return "Internal Server Error",500

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
                    q.update({"username":str(modified_username),"password":str(modified_password)})
                    db.session.commit()
                elif not uname_valid:
                    return "Modified Username is invalid",400
                elif not pass_valid:
                    return "Modified Password is invalid",400

            return self.get(modified_username)
        except:
            return "Internal Server Error",500

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
                    new_user=User(username=str(data['username']),password=str(data['password']),fs_uniquifier=bcrypt.gensalt())
                    db.session.add(new_user)
                    db.session.commit()
                elif not username_valid(data['username']):
                    return "Username is invalid",400
                elif not password_valid(data['password']):
                    return "Password is invalid",400
            return self.get(data['username'])
        except Exception as e:
            return "Internal Server Error",500

class TrackerApi(Resource):

    def get(self,tracker_id):
        try:
            trk=tracker.query.get(tracker_id)
            if trk==None:
                return "Tracker id not found",404
            return marshal(trk,tracker_fields)
        except:
            return "Internal Server Error",500

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
            if ttype!="Multi-choice":
                tset=""
            elif ("," not in tset):
                 return "tracker settings should be given for type multi-choice which are options that must be separated with comma.",400
            if tnv and ttv:
                tobj=tracker(user_id=int(uid),name=str(tname),desc=str(tdesc),type=str(ttype),settings=str(tset))
                db.session.add(tobj)
                db.session.commit()
                return marshal(tobj,tracker_fields),200
            elif not tnv:
                return "tracker name not valid",400
            elif not ttv:
                return "tracker type not valid",400
        except:
            return "Internal Server Error",500

    def put(self,tracker_id):
        try:
            pdata=request.json
            tname=pdata["modified_tracker_name"]
            ttype=pdata["modified_tracker_type"]
            tset=pdata["modified_tracker_settings"]
            q=db.session.query(tracker).filter(tracker.tracker_id==tracker_id)
            if q.first()==None:
                return "Tracker id not found",404
            if ttype!=q.first().type:
                pass
            if ttype!="Multi-choice":
                    tset=""
            elif ("," not in tset):
                        return "tracker settings should be given for type multi-choice which are options that must be separated with comma.",400
            update_dict={"name":tname,
            "desc":pdata["modified_tracker_description"],
            "type":ttype,
            "settings":tset,
            }
            if tracker_name_valid(tname) and tracker_type_valid(ttype):
                q.update(update_dict)
                db.session.commit()
            elif not tracker_name_valid(tname):
                return "name not valid",400
            elif not tracker_type_valid(ttype):
                return "tracker type not valid",400
            return marshal(q.first(),tracker_fields)
        except:
            return "Internal Server Error",500



    def delete(self,tracker_id):
        tobj=tracker.query.get(tracker_id)
        tlogs=log.query.filter(log.tracker_id==tracker_id).all()
        db.session.delete(tobj)
        db.session.commit()
        return "OK",200

class LogApi(Resource):
    def get(self,log_id):
        pass
    def put(self,log_id):
        pass
    def delete(self,log_id):
        pass
    def post(self):
        pass
#===========Api===========
