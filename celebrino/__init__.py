from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import os

app = Flask(__name__)
app.secret_key = 'The secret to backdoor'
app.config['SECRET_KEY'] = 'Trolific.com/celebrino'

#To Upload files
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/venue')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_GALLERY = {'jpg','jpeg','mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#Tokenization
s = URLSafeTimedSerializer("Thisismyscrete")

#Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql6521945:VyPeZUxFa1@sql6.freemysqlhosting.net:3306/sql6521945'
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
