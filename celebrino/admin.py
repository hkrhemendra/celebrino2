from flask import redirect,render_template,request
from celebrino import db,bcrypt
from celebrino.model import Cakes, Gallery, Venue
import random
from celebrino.tools import send_mail, upload_file, upload_gallery_file

def venue_approve(id):
    venue = Venue.query.filter_by(venue_id = id).first()
    # password = str(random.randint(10000000,99999999))
    password = str(12345678)
    pw_hash = bcrypt.generate_password_hash(password)

    body = "Congratulations, Your Venue has been approved by Celebrino team. Now you can login to your dashboard and complete your profile. \nYour login credentials are:\nusername: {} \npassword:{} ".format(venue.email,password)

    send_mail("Celebrino","Your Venue has been approve by Celebrino","hemendrafakelalawat@gmail.com",venue.email,body)

    venue.verified = True
    venue.password = pw_hash
    db.session.commit()
    return redirect('/venue_request')

def gallery_upload():
    if request.method == 'POST':
        file = request.files['file']
        item_type = request.form.get('item_type')
        poster = request.files['poster_file']
        
        if item_type == 'image':
            upload_gallery_file(file,item_type)
            entry = Gallery(file_name = file.filename, type = item_type)
            db.session.add(entry)
            db.session.commit()
        else:
            upload_gallery_file(file,item_type)
            upload_gallery_file(poster,'poster')
            entry = Gallery(file_name = file.filename, type = item_type, poster = poster.filename)
            db.session.add(entry)
            db.session.commit()

        return redirect('/upload_items')

def cake_upload():
    if request.method ==  'POST':
        title = request.form.get('cake_title')
        description = request.form.get('cake_description')
        price = request.form.get('cake_price')
        file = request.files['file']
        
        upload_gallery_file(file,'cake')

        entry = Cakes(title=title,description=description,price=price,picture=file.filename)
        db.session.add(entry)
        db.session.commit()

    return redirect('/upload_items')