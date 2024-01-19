import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
import datetime


class Transaction(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    coin_change = Column(Integer)
    comment = Column(String)
    transaction_time = Column(sqlalchemy.DateTime,
                              default=datetime.datetime.now)
    item_id = Column(Integer, ForeignKey('users.id'))


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    card_id = Column(String)
    coins = Column(Integer)
    email = Column(String)
    password = Column(String)
    status = Column(Integer)

    def set_password(self, password):   # смена пароля
        self.password = generate_password_hash(password)

    def check_password(self, password):  # проверка пароля
        return check_password_hash(self.password, password)

    def check_admin(self):
        if self.status == 3:
            return True
        return False

    def check_teacher(self):
        if self.status == 2:
            return True
        return False


class Item(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    quantity = Column(Integer)
    description = Column(String)
    price = Column(Integer)

    def reduce_quantity(self):
        self.quantity = self.quantity - 1


