from datetime import datetime
from celebrino import db,app



class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    verified = db.Column(db.Integer, nullable= True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(100), nullable=False)


class Venue(db.Model):
    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    venue_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(70), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    venue_type = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=True)
    verified = db.Column(db.Integer, nullable= True)


class Locatedocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer,db.ForeignKey('venue.venue_id') ,nullable=False)
    gumasta = db.Column(db.String(50), nullable=False)
    fssai = db.Column(db.String(50), nullable=False)
    picture1 = db.Column(db.String(50), nullable=True)
    picture2 = db.Column(db.String(50), nullable=True)
    picture3 = db.Column(db.String(70), nullable=True)
    picture4 = db.Column(db.String(20), nullable=True)

class Menu(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    price = db.Column(db.String(30), nullable=False)
    item_type = db.Column(db.String(30), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(30), nullable=False)

class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'), nullable = False)
    venue_id = db.Column(db.Integer,db.ForeignKey('venue.venue_id'),nullable = False)
    event_type = db.Column(db.String(30),default='dinein')
    time = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date, nullable=False)
    guests = db.Column(db.String(20), nullable=True)
    bill = db.Column(db.String(30), nullable=True)
    order_status = db.Column(db.String(20), nullable=False)
    discount = db.Column(db.String(30), nullable=True)
    age_group = db.Column(db.String(50), nullable=True)
    cake = db.Column(db.String(50), nullable=True)

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable = False)
    role = db.Column(db.String(50),nullable = False)
    password = db.Column(db.String(100),nullable=False)

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer,nullable=False )
    review_title = db.Column(db.String(50), nullable=False)
    food_quality = db.Column(db.String(50), nullable=False)
    service = db.Column(db.String(50), nullable=False)
    hygiene = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    review = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable = False)
    blog = db.Column(db.String(200),nullable = False)
    timestamp = db.Column(db.DateTime,nullable=False)
    slug = db.Column(db.String(70),nullable = False)
    picture = db.Column(db.String(30),nullable = False)


class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(70), nullable = False)
    type = db.Column(db.String(20),nullable = False)
    poster = db.Column(db.String(50),nullable = True)

class Cakes(db.Model):
    cake_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable = False)
    description = db.Column(db.String(70),nullable = False)
    price = db.Column(db.String(20), nullable = False)
    picture = db.Column(db.String(60),nullable = False)
    

db.create_all()
db.session.commit()