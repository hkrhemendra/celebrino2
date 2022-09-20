from celebrino.tools import upload_file
from os import name
import re
from werkzeug.utils import secure_filename
from flask.helpers import flash, url_for
from celebrino.views import confirmation_email, password_recover
from flask import request,render_template,redirect, session
from celebrino import db,bcrypt
from celebrino.model import Admin, Cakes, Locatedocument, Menu, Venue

def signin_venue():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        venue = Venue.query.filter_by(email=email).first()
        if venue is not None:
            if bcrypt.check_password_hash(venue.password,password):
                session['venue_id'] = venue.venue_id
                return redirect('/venue_dashboard')
            message = "Invalid Password. Please try again"
            return render_template('venue_login.html',message=message)
        if email == 'admin@gmail.com':
            admin = Admin.query.filter_by(username = email).first()
            if bcrypt.check_password_hash(admin.password,password):
                session['admin_id'] = admin.admin_id
                return redirect('/admin')
        message = "Invalid Email. Please check you email or register your venue"
        return render_template('venue_login.html',message=message)

def profile_venue():
    venue_id = session['venue_id']
    venue = Venue.query.filter_by(venue_id=venue_id).first()
    name = venue.venue_name.capitalize()
    phone = venue.phone.capitalize()
    email = venue.email.capitalize()
    type = venue.venue_type.capitalize()
    address = venue.address.capitalize()
    return render_template('admin/user-profile.html',name=name,phone=phone,email=email,type=type,address=address)

def venue_password_update():
    if request.method == 'POST':
        old_pass = request.form.get('old_pass')
        new_pass = request.form.get('new_pass')
        confirm_pass = request.form.get('confirm_pass')
        print(old_pass,new_pass,confirm_pass)

        if new_pass != confirm_pass:
            flash("Your New password and confirm password doesn't match")
            return redirect('/venue_profile')
        
        venue_id = session['venue_id']
        venue = Venue.query.filter_by(venue_id=venue_id).first()
        if bcrypt.check_password_hash(venue.password,old_pass):
            pw_hash = bcrypt.generate_password_hash(new_pass)
            venue.password = pw_hash
            db.session.commit()
            flash("Your password has been updated.")
            return redirect('/venue_profile')
        
        flash('Your old password is invalid')
        return redirect('/venue_profile')

def menu_submit():
    if request.method == 'POST':
        venue_id = session['venue_id']
        title = request.form.get('item_title')
        price = request.form.get('item_price')
        item_type = request.form.getlist('options')
        category = request.form.get('item_category')
        description = request.form.get('item_description')
        picture=request.files['picture']

        picture_name = picture.filename
        
        entry = Menu(venue_id=venue_id,title=title,price=price,category=category,item_type=item_type,description=description,picture=picture_name)
        db.session.add(entry)
        db.session.commit()
        
        venue = Venue.query.filter_by(venue_id=venue_id).first()
        name = venue.venue_name
        upload_file(picture,name,'menu')

        return redirect('/add_menu')
    return 'get'

def venue_picture():
    if request.method == 'POST':
        picture1 = request.files['picture1']
        picture2 = request.files['picture2']
        picture3 = request.files['picture3']
        picture4 = request.files['picture4']
        
        venue_id = session['venue_id']
        venue = Venue.query.filter_by(venue_id=venue_id).first()
        upload_file(picture1,venue.venue_name,'pictures')
        upload_file(picture2,venue.venue_name,'pictures')
        upload_file(picture3,venue.venue_name,'pictures')
        upload_file(picture4,venue.venue_name,'pictures')

        picture = Locatedocument.query.filter_by(venue_id = venue_id).first()
        picture.picture1 = picture1.filename
        picture.picture2 = picture2.filename
        picture.picture3 = picture3.filename
        picture.picture4 = picture4.filename
        db.session.commit()

        return redirect('/venue_profile')


def details_venue(venue_id):
    venue_detail = Venue.query.filter_by(venue_id=venue_id).first()
    venue_picture = Locatedocument.query.filter_by(venue_id=venue_id).first()
    menu = Menu.query.filter_by(venue_id=venue_id).all()
    cakes = Cakes.query.all()
    return render_template('venue_details.html',venue_detail=venue_detail,venue_picture=venue_picture,menu=menu,cakes=cakes)
