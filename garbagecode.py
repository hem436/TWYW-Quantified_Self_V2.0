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
