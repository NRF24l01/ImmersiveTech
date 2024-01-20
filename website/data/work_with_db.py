import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), )
    coin_change = Column(Integer)
    comment = Column(String)
    transaction_time = Column(sqlalchemy.DateTime,
                              default=datetime.datetime.now)
    item_id = Column(Integer, ForeignKey('items.id', ondelete='CASCADE'))
    item = relationship('Item', backref='transactions', cascade='all, delete-orphan', single_parent=True)
    user = relationship('User', backref='transactions', cascade='all, delete-orphan', single_parent=True)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    card_id = Column(String)
    coins = Column(Integer)
    email = Column(String)
    password = Column(String)
    status = Column(Integer, default=1)
    transaction = relationship('Transaction', back_populates='user')

    def set_password(self, password: str):   # смена пароля
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:  # проверка пароля
        return check_password_hash(self.password, password)

    def check_admin(self) -> bool:
        if self.status == 3:
            return True
        return False

    def check_teacher(self) -> bool:
        if self.status == 2:
            return True
        return False

    def change_status(self, difference: int) -> bool:
        if 1 <= self.status + difference <= 3:
            self.status = self.status + difference
            return True
        return False

    def add_coins(self, amount: int):
        self.coins += amount

    def transfer_coins(self, amount: int):
        self.coins -= amount


class Item(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image = Column(String)
    quantity = Column(Integer)
    description = Column(String)
    price = Column(Integer)
    transaction = relationship('Transaction', back_populates='item')

    def reduce_quantity(self):
        self.quantity = self.quantity - 1


class Task(db.Model):
    __tablename__ = 'awards_achievements'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    qualifications = Column(String)
    award = Column(Integer)
    grade = Column(String)

    def add_qualifications(self, qualifications: list[str]):
        self.qualifications += qualifications
        self.qualifications = list(set(self.qualifications))

    def remove_qualifications(self, qualifications: list[str]):
        for elem in qualifications:
            try:
                self.qualifications.remove(elem)
            except Exception:
                continue