from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import os
import sshtunnel

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

tunnel = sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'), ssh_username='hemendra123',ssh_password = 'Hemendra@123',
    remote_bind_address=('hemendra123.mysql.pythonanywhere-services.com', 3306)

)

#Flask app
app = Flask(__name__)
app.secret_key = 'The secret to backdoor'
app.config['SECRET_KEY'] = 'Trolific.com/celebrino'

#To Upload files
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/venue')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_GALLERY = {'jpg','jpeg','mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

tunnel.start()

#Tokenization
s = URLSafeTimedSerializer("Thisismyscrete")

#Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://hemendra123:celebrino123@hemendra123.mysql.pythonanywhere-services.com/hemendra123$default'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


db.create_all()
db.session.commit()


        


# Bcrypt
bcrypt = Bcrypt(app)

#Mail service
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hemendrafakelalawat@gmail.com'
app.config['MAIL_PASSWORD'] = 'ofunincmfnikydvv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
