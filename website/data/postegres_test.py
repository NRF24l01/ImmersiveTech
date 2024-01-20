import uuid
from flask import render_template, request, redirect, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user_forms import *
from db_session import *
from website.data import db_session
from work_with_db import User, Transaction, Item, Task
import uuid
from flask import render_template, request, redirect, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


db_sess = db_session.create_session()
user = User(
    name='Kirill',
    surname='Fedotov',
    card_id='2r33reff',
    coins=500,
    email='fedotovkirill4000@gmail.com',
    grade=5,
    status=2
)
user.set_password(request.args.get('password'))
db_sess.add(user)
db_sess.commit()
