from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from passwords import *
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = app_password  # секретный ключ из файла passwords
db_string = "postgresql://{}:{}@{}:{}/{}".format(db_name, db_password,
                                                 '192.168.115.201', 5432, 'school_bank')
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
db_session.global_init("db/database.db")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
