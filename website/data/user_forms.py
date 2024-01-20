from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):    # форма логина
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):   # форма регистрации
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    card_id = StringField('Карта пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class ResetPasswordForm(FlaskForm):   # форма восстановления пароля
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Восстановить доступ')


class CreateTaskForm(FlaskForm):   # форма восстановления пароля
    task_name = StringField('Название задания', validators=[DataRequired()])
    reward = IntegerField('Награда за выполнение', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    grade = StringField(label='Класс в формате - "ЧислоБуква"', validators=[DataRequired()])
    submit = SubmitField('Создать задание')

