
from celebrino import venue
from celebrino.tools import search_keyword
from celebrino.venue import details_venue, menu_submit, profile_venue, signin_venue, venue_password_update, venue_picture
from celebrino.admin import  cake_upload, gallery_upload, venue_approve
from celebrino.model import Gallery, Locatedocument, Orders,  Users, Venue
from flask import render_template,redirect,session
from celebrino import app,db
from celebrino.views import  booking_list, context_user, index_page, order_cancel, pass_recover, pass_update, review_submit, sign_up,sign_in,send_enquiry,confirmation_email,password_recover, venue_book, venue_book_dine, venue_date

@app.context_processor
def inject_user():
    return context_user()

@app.route('/')
def index():
    return index_page()

@app.route('/search',methods=['POST'])
def search():
    return search_keyword()

# Login Page
@app.route('/login')
def login():
    return render_template('login.html')

# Login Function
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    return sign_in()

# logout function
@app.route('/logout')
def logout():
    # session.pop('user_id',None)
    session.clear()
    return redirect('/')

# Register Page
@app.route('/register')
def register():
    return render_template('register.html')

# Sign up function
@app.route('/signup',methods=['GET','POST'])
def signup():
    return sign_up()

# contact form 
@app.route('/contact')
def contact():
    return render_template('contacts.html')

# Contact function
@app.route('/sendenquiry',methods=['GET','POST'])
def sendenquiry():
    return send_enquiry()

# Email confirmation 
@app.route('/email_confirmation/<token>')
def email_confirmation(token):
    return confirmation_email(token)

# forget password 
@app.route('/forget_password')
def forget_password():
    return render_template('sign.html')

# To recover password page
@app.route('/recover_password',methods=['POST'])
def recover_password():
    return password_recover()

# Email recover pass
@app.route('/recover_pass/<token>')
def recover_pass(token):
    return pass_recover(token)

# To update pass pa
@app.route('/update_pass',methods=['POST','GET'])
def update_pass():
    return pass_update()

# Open venue Registration page
@app.route('/add_venue')
def add_venue():
    return render_template('submit-restaurant.html')

@app.route('/register_venue')
def register_venue():
    return render_template('register_venue.html')

@app.route('/upload_venue_data',methods=['POST','GET'])
def upload_venue_data():
    return venue_date()

@app.route('/bookings')
def bookings():
    return booking_list()

@app.route('/cancel_order/<order_id>')
def cancel_order(order_id):
    return order_cancel(order_id)

@app.route('/cafes')
def cafes():
    venues = db.session.query(Venue,Locatedocument).join(Locatedocument).filter(Venue.venue_type == 'cafe').all()
    return render_template('venue_list.html',venues=venues)

@app.route('/restaurants')
def restaurants():
    venues = db.session.query(Venue,Locatedocument).join(Locatedocument).filter(Venue.venue_type == 'restaurant').all()
    return render_template('venue_list.html',venues=venues)

@app.route('/hotels')
def hotels():
    venues = db.session.query(Venue,Locatedocument).join(Locatedocument).filter(Venue.venue_type == 'hotel').all()
    return render_template('venue_list.html',venues=venues)

@app.route('/organize_event')
def organize_event():
    venues = db.session.query(Venue,Locatedocument).join(Locatedocument).all()
    return render_template('venue_list.html',venues=venues)


@app.route('/venue_details/<venue_id>')
def venue_details(venue_id):
    return details_venue(venue_id)


@app.route('/book_venue',methods=['GET','POST'])
def book_venue():
    return venue_book()

@app.route('/book_venue_dine', methods=['GET', 'POST'])
def book_venue_dine():
    return venue_book_dine()

@app.route('/leave_review/<venue_id>')
def leave_review(venue_id):
    return render_template('leave-review.html',venue_id=venue_id)

@app.route('/submit_review', methods=['GET', 'POST'])
def submit_review():
    return review_submit()


@app.route('/gallery_videos')
def gallery():
    gallery = Gallery.query.filter_by(type='video')
    return render_template('gallery.html',gallery=gallery,type='image')

@app.route('/gallery_pictures')
def pictures():
    gallery = Gallery.query.filter_by(type='image')
    return render_template('gallery.html',gallery=gallery,type='image')

#Venue section

@app.route('/venue_login')
def venue_login():
    return render_template('venue_login.html')

@app.route('/venue_signin',methods=['GET','POST'])
def venue_signin():
    return signin_venue()

@app.route('/venue_dashboard')
def venue_dashboard():
    if 'venue_id' not in session:
        return redirect('/venue_login')
    venue_id = session['venue_id']
    pending_orders = Orders.query.filter_by(venue_id=venue_id,order_status='pending').count()
    complete_orders = Orders.query.filter_by(venue_id=venue_id,order_status='complete').count()
    total_orders = Orders.query.filter_by(venue_id=venue_id).count()
    return render_template('admin/venue_dashboard.html',pending_orders=pending_orders,complete_orders=complete_orders,total_orders=total_orders)

@app.route('/venue_profile')
def venue_profile():
    if 'venue_id' not in session:
        return redirect('/venue_login')
    return profile_venue()

@app.route('/update_venue_password',methods=['GET','POST'])
def update_venue_password():
    if 'venue_id' not in session:
        return redirect('/venue_login')
    return venue_password_update()


@app.route('/add_menu')
def add_menu():
    if 'venue_id' not in session:
        return redirect('/venue_login')
    return render_template('admin/add_menu.html')

@app.route('/submit_menu', methods=['GET', 'POST'])
def submit_menu():
    return menu_submit()

@app.route('/upload_venue_picture', methods=['GET', 'POST'])
def upload_venue_picture():
    return venue_picture()

@app.route('/pending_orders')
def pending_orders():
    if 'venue_id' not in session:
        return redirect('/venue_login')
    venue_id = session['venue_id']
    orders = db.session.query(Users,Orders).join(Orders).filter(Orders.order_status=='pending',Orders.venue_id==venue_id).all()
    return render_template('admin/orders.html',orders=orders)


@app.route('/complete_orders')
def complete_orders():
    if 'venue_id' not in session:
        return redirect('/venue_login')
    venue_id = session['venue_id']
    orders = db.session.query(Users,Orders).join(Orders).filter(Orders.order_status=='complete',Orders.venue_id==venue_id).all()
    return render_template('admin/orders.html',orders=orders)

@app.route('/all_orders')
def all_orders():
    if 'venue_id' not in session:
        return redirect('/venue_login')
    venue_id = session['venue_id']
    orders = db.session.query(Users,Orders).join(Orders).filter(Orders.venue_id==venue_id).all()
    return render_template('admin/orders.html',orders=orders)


# admins section
@app.route('/admin')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect('/venue_login')
    return  render_template('admin/dashboard.html')

@app.route('/venue_request')
def venue_request():
    if 'admin_id' not in session:
       return redirect('/venue_login')
    venue_request = db.session.query(Venue,Locatedocument).join(Locatedocument).filter(Venue.verified == 0).all()
    return render_template('admin/venue_request.html',venue_request=venue_request)

@app.route('/venue_list')
def venue_list():
    if 'admin_id' not in session:
        return redirect('/venue_login')
    venues = Venue.query.all()
    return render_template('admin/venue.html',venues=venues)

@app.route('/approve_venue/<id>')
def approve_venue(id):
    if 'admin_id' not in session:
        return redirect('/venue_login')
    return venue_approve(id)

@app.route('/admin_pending_orders')
def admin_pending_orders():
    if 'admin_id' not in session:
        return redirect('/venue_login')
    role = 'admin'
    orders = db.session.query(Users,Orders).join(Orders).filter(Orders.order_status=='pending').all()
    return render_template('admin/orders.html',orders=orders,role=role)

@app.route('/admin_complete_orders')
def admin_complete_orders():
    if 'admin_id' not in session:
        return redirect('/venue_login')
    role = 'admin'
    orders = db.session.query(Users,Orders).join(Orders).filter(Orders.order_status=='complete').all()
    return render_template('admin/orders.html',orders=orders,role=role)


@app.route('/admin_all_orders')
def admin_all_orders():
    if 'admin_id' not in session:
        return redirect('/venue_login')
    role = 'admin'
    orders = db.session.query(Users,Orders).join(Orders).all()
    return render_template('admin/orders.html',orders=orders,role=role)


@app.route('/upload_items')
def upload_items():
    if 'admin_id' not in session:
        return redirect('/venue_login')
    return render_template('admin/upload_items.html')

@app.route('/upload_gallery', methods=['GET','POST'])
def upload_gallery():
    return gallery_upload()

@app.route('/upload_cake', methods=['GET','POST'])
def upload_cake():
    return cake_upload()

# Blog section
@app.route('/blogs')
def blogs():
    return render_template('blog.html')
