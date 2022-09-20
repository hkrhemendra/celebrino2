from celebrino import ALLOWED_EXTENSIONS_GALLERY, mail, ALLOWED_EXTENSIONS,db
from flask_mail import Message
import os
from flask import flash, session,url_for,redirect,render_template,request
from werkzeug.utils import secure_filename
from celebrino.model import Venue,Locatedocument
from operator import or_

def send_mail(name,subject,sender,recipients,body):
    msg = Message(subject=subject, sender = sender, recipients = [recipients])
    msg.body = "Name: {}. \nMessage: {}".format(name,body)
    mail.send(msg)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file,venue_name,path):   
    new_venue_name =venue_name.replace(' ','_')       
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('register_venue'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/venue/')
        try:
            os.makedirs(upload_path+new_venue_name)
            os.makedirs(upload_path+new_venue_name+'/documents')
            os.makedirs(upload_path+new_venue_name+'/menu')
            os.makedirs(upload_path+new_venue_name+'/pictures')
            file.save(os.path.join(upload_path+new_venue_name + '/' + path, filename))
        except FileExistsError:
            file.save(os.path.join(upload_path+new_venue_name + '/' + path , filename))


def allowed_gallery_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_GALLERY

def upload_gallery_file(file,item_type):   
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('register_venue'))
    if file and allowed_gallery_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = 'D:\\Celebroz\\fooyes_v.1.3\\Flask\\celebrino\\static\\gallery\\'
        try:
            if item_type == 'image':
                file.save(os.path.join(upload_path+ '\\images', filename))
            elif item_type == 'cake':
                file.save(os.path.join(upload_path+ '\\cakes', filename))
            elif item_type == 'poster':
                file.save(os.path.join(upload_path+ '\\videos\\poster', filename))
            else:
                file.save(os.path.join(upload_path+ '\\videos', filename))
        except FileExistsError:
            return 'Cannot create folder File already exist'


def search_keyword():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        print(keyword)
        venues = db.session.query(Venue,Locatedocument).join(Locatedocument).filter(or_(Venue.venue_name.like(keyword+ "%"),Venue.address.like(keyword+ "%"))).all()
        if venues is not None:
            return render_template('venue_list.html',venues=venues)
        message = "No search result found"
        flash(message)
        return render_template('venue_list.html')

