from operator import add
import flask
from flask.helpers import url_for
from flask.json import loads
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from celebrino.tools import send_mail,allowed_file,upload_file
from celebrino.model import Orders, Review, Users,Venue,Locatedocument
from flask import flash,redirect,render_template,request,session
from celebrino.model import Users,Contact
from celebrino import db,bcrypt,s,app, venue
from itsdangerous import SignatureExpired,BadSignature
from werkzeug.utils import secure_filename
import os
from datetime import datetime


def index_page():
    popular = db.session.query(Venue,Locatedocument).join(Locatedocument).filter(Venue.category=='popular').all()
    hotel = db.session.query(Venue,Locatedocument).join(Locatedocument).filter(Venue.category=='popular',Venue.venue_type=='hotel').limit(3).all()
    cafe = db.session.query(Venue,Locatedocument).join(Locatedocument).filter(Venue.category=='popular',Venue.venue_type=='cafe').limit(3).all()
    restaurant = db.session.query(Venue,Locatedocument).join(Locatedocument).filter(Venue.category=='popular',Venue.venue_type=='restaurant').limit(3).all()

    return render_template('index.html',popular=popular,hotel=hotel,cafe=cafe,restaurant=restaurant)


def sign_up():
    if request.method == 'POST':
        
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password == confirm_password:
            user = Users.query.filter_by(email=email).first()
            check_phone = Users.query.filter_by(phone=phone).first()
            #Check if email already exist
            if user is None:
                if check_phone is None:
                    password_hash = bcrypt.generate_password_hash(password)
                    entry = Users(firstname=firstname,lastname=lastname,email=email,phone=phone,password=password_hash,verified=0)
                    db.session.add(entry)
                    db.session.commit()
                    
                    verification_token = s.dumps(email,salt='email-confirmation')
                    verification_link = url_for('email_confirmation',token=verification_token, _external=True )

                    send_mail(firstname,"Email Verfication","hemendrafakelalawat@gmail.com",email,"Click on this link to verify your account. \n {}".format(verification_link))

                    message = "You are registered successfully. Please check your email to verify the account. Thank you."
                    return render_template('register.html',message = message)
                message = "Your mobile no is already registered."
                return render_template('register.html',message = message)
            #Check email to registered email 

            if user.verified == 0:
                verification_token = s.dumps(email,salt='email-confirmation')
                verification_link = url_for('email_confirmation',token=verification_token, _external=True )
                send_mail(firstname,"Email Verfication","hemendrafakelalawat@gmail.com",email,"Click on this link to verify your account. \n {}".format(verification_link))
                message = "Your account is already registered with this email. Kindly verify it."
                return render_template('register.html',message = message)
            # SHow message 
            message = "Your account is registered already. Please login."
            return render_template('register.html',message = message)

        message = "Your password doesn't match"
        return render_template('register.html', message=message)

def confirmation_email(token):
    try:
        email = s.loads(token,salt='email-confirmation',max_age=300)
        user = Users.query.filter_by(email=email).first()
        user.verified = 1
        db.session.commit()
        return redirect('/')
    except SignatureExpired:
        return render_template('register.html',message="Token has been expired please try again")
    except BadSignature:
        return render_template('register.html',message="The token is invalid")


def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if 'user_id' in session:
            message = ' You are already logged in '
            return render_template('login.html',message=message)

        if user != None:
            if user.verified == 1:
                print("Password: {}".format(user.password))
                if bcrypt.check_password_hash(user.password,password):
                    session['user_id'] = user.user_id
                    return redirect('/')
                message = "Please check you password"
                return render_template('login.html',message=message)
            
            message = "Your email address is not verified. please register again with same email to verify email"
            return render_template('login.html', message=message)

        message = "Your email doesn't exist. Please check your email or Kindly register it"
        return render_template('login.html', message=message)




def send_enquiry():
    if request.method == 'POST':
        name = request.form.get('name_contact')
        email = request.form.get('email_contact')
        message = request.form.get('message_contact')

        send_mail(name,"Enquiry Alert",email,"hemendralalawat30@gmail.com",message)

        entry = Contact(name=name,email=email,message=message)
        db.session.add(entry)
        db.session.commit()

        flash('Your response has been submitted')
        return redirect('/contact')

def password_recover():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Users.query.filter_by(email = email).first()
        print("Users: {}".format(user))
        if user is not None:
            token = s.dumps(email,salt="recoverpassword")
            recovery_link = url_for('recover_pass',token=token,_external=True)
            body = "Click on this link to recover your password.\nLink: {}".format(recovery_link)
            send_mail("Celebrino","Recovery Email","hemendrafakelalawat@gmail.com",email,body)
            message = "A recovery link has been sent to you account please check."
            return render_template('sign.html',message=message)

        message = "Your email is not registered Please sign up."
        return render_template('sign.html',message=message)
    return "success"

def pass_recover(token):
    try:
        email = s.loads(token,salt='recoverpassword',max_age=300)
        user = Users.query.filter_by(email=email).first()
        id = user.user_id
        return render_template('update_pass.html',id=id)
    except SignatureExpired:
        return render_template('register.html',message="Token has been expired please try again")
    except BadSignature:
        return render_template('register.html',message="The token is invalid")

def pass_update():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password =request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password == confirm_password:
            user = Users.query.filter_by(user_id=user_id).first()
            user.password = bcrypt.generate_password_hash(password)
            db.session.commit()
            return redirect('/login')
        message = "Your password doesn't match"
        return render_template('update_pass.html',message=message)

def venue_date():
    if request.method == 'POST':
        #form field variable
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        venue_name = request.form.get('venue_name')
        address = request.form.get('address')
        city = request.form.get('city')
        venue_type = request.form.get('type')
        #form file variable
        gumasta = request.files['gumasta']
        fssai = request.files['fssai']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        check_venue = Venue.query.filter_by(venue_name=venue_name,city=city).first()
        if check_venue is not None:
            flash("Venue already Exist")
            return redirect('register_venue')

        upload_file(gumasta,venue_name.strip(),'documents')
        upload_file(fssai,venue_name.strip(),'documents')

        #updating to database
        venue_entry = Venue(name=name,email=email,phone=phone,venue_name=venue_name,address=address,city=city,venue_type=venue_type,category='new',verified=False)
        db.session.add(venue_entry)
        db.session.commit()

        venue_detail = Venue.query.filter_by(venue_name=venue_name).first()
        venue_id = venue_detail.venue_id
        document_entry = Locatedocument(venue_id=venue_id,gumasta=gumasta.filename,fssai=fssai.filename)
        db.session.add(document_entry)
        db.session.commit()

        
        flash(" You are registered successfully. Please wait till your doucments get verified. We will update you through mail. ")
        return redirect('register_venue')
    return 'get'

def context_user():
    if 'user_id' in session:
        user_id = session['user_id']
        user = Users.query.filter_by(user_id=user_id).first()
        firstname = user.firstname
        lastname = user.lastname
        username = "{} {}".format(firstname,lastname)
        return dict(key=username)
    else:
        username = 'null'
        return dict(key=username)

def venue_book():
    if request.method == 'POST':
        
        if 'user_id' not in session:
            return redirect('/login')

        user_id = session['user_id']
        venue_id = request.form.get('venue_id')
        guests = request.form.get('guests')
        time = request.form.get('time')
        date = request.form.get('date')
        order_status = 'pending'
        event_type = request.form.get('event_type')
        cake = request.form.get('cake')
        age_group = request.form.get('age_group')

        print(event_type)
        entry = Orders(user_id=user_id,venue_id=venue_id,time=time,date=date,guests=guests,order_status=order_status,event_type=event_type,cake=cake,age_group=age_group)
        db.session.add(entry)
        db.session.commit()
        
        return redirect('/bookings')

def venue_book_dine():
        if 'user_id' not in session:
            return redirect('/login')

        user_id = session['user_id']
        venue_id = request.form.get('venue_id')
        time = request.form.get('time')
        date = request.form.get('date')
        order_status = 'pending'
        event_type = 'dinein'


        print(event_type)
        entry = Orders(user_id=user_id,venue_id=venue_id,time=time,date=date,order_status=order_status,event_type=event_type)
        db.session.add(entry)
        db.session.commit()
        return redirect('/bookings')


def review_submit():
    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect('/login')
        user_id = session['user_id']
        venue_id = request.form.get('venue_id')
        review = request.form.get('review')
        food_quality = request.form.get('food_quality')
        service = request.form.get('service')
        hygiene = request.form.get('hygiene')
        price = request.form.get('price')
        review_title = request.form.get('review_title')
        timestamp = datetime.now()

        print( user_id,venue_id,review,food_quality,service,hygiene,price,review_title,timestamp)

        entry = Review(user_id=user_id,venue_id=venue_id,review_title=review_title,timestamp=timestamp,food_quality=food_quality,service=service,hygiene=hygiene,price=price,review=review)
        db.session.add(entry)
        db.session.commit()

        return redirect('/')

def booking_list():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    bookings = db.session.query(Orders,Venue).join(Venue).filter(Orders.user_id == user_id).all()
    return render_template('bookings.html',bookings=bookings)

def order_cancel(order_id):
    update_order = Orders.query.filter_by(order_id=order_id).first()
    venue_email = Venue.query.filter_by(venue_id = update_order.venue_id).first()
    send_mail('Celebrino','Order Cancel','sheowest@gmail.com',venue_email.email,"The order has been cancelled with order id {}. \n The date of order was {}".format(order_id,update_order.date))
    update_order.order_status = 'Cancelled'
    db.session.commit()
    return redirect('/bookings')