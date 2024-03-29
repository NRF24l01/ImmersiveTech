import uuid
from manage import *
from flask import render_template, request, redirect, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.user_forms import *
from data.work_with_db import User, Transaction, Item, Task
import datetime
import app_api
from data.user_forms import RegisterForm, LoginForm

app.register_blueprint(app_api.blueprint)  # подлючение api
login_manager = LoginManager()  # подключение flask_login
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):  # подгрука пользователя из бд
    try:
        db_sess = db_session.create_session()
        return db_sess.query(User).get(user_id)
    except Exception:
        return None


@app.route('/', methods=["POST", "GET"])
def main_page():  # главная страница
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    if request.method == 'POST':
        if request.form.get("support"):
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")
            print(f"support {name} {email} {message}")
            return redirect('/')
        else:
            email = request.form.get("email_ad")
            print(f"subscribe {email}")
            return redirect('/')
    return render_template('index.html',
                           logged=current_user.is_authenticated,
                           teacher=teacher)


@app.route('/login', methods=["POST", "GET"])
def login_page():  # страница входа
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):  # получние пароля по почте и сравнение
            login_user(user)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, teacher=teacher)
    return render_template('login.html', form=form, teacher=teacher)


@app.route('/create-task', methods=["POST", "GET"])
@login_required
def create_task():  # создание задания
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    if load_user(current_user).check_teacher():
        form = CreateTaskForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            # подключение бд и проверка наличия почты там
            if db_sess.query(Task).filter(Task.name == form.task_name.data).first():
                return render_template('create_task.html',
                                       form=form,
                                       message="Такое задание уже есть",
                                       teacher=teacher)
            task = Task(
                name=form.task_name.data,
                description=form.description.data,
                qulifications=form.description.data,
                award=form.reward.data,
                grade=form.grade.data
            )
            db_sess.add(task)  # добавление в бд
            db_sess.commit()
            return redirect("/tasks")
        return render_template('create_task.html', form=form,
                               teacher=teacher)
    return redirect('/')


@app.route('/check_tasks', methods=["GET", "POST"])
@login_required
def check_tasks():
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    db_sess = db_session.create_session()
    data = db_sess.query(Task).all()
    users = db_sess.query(User).all()
    if request.method == 'POST':
        if request.form.get('btn'):
            task = db_sess.query(Task).filter(Task.id == int(request.form.get('btn'))).first()
            user = db_sess.query(User).filter(User.name == request.form.get('student')).first()
            user.add_coins(task.award)
            db_sess.commit()
        return render_template('asses.html', logged=current_user.is_authenticated,
                               data=data, users=users, teacher=teacher)
    return render_template('asses.html', logged=current_user.is_authenticated, data=data, users=users,
                           teacher=teacher)


@app.route('/logout')
@login_required
def logout():
    logout_user()  # выход из аккаунта
    return redirect("/")


@app.route('/register', methods=["POST", "GET"])
def register_page():  # страница регистрации
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('signup.html',
                                   form=form,
                                   message="Пароли не совпадают", teacher=teacher)
        db_sess = db_session.create_session()
        # подключение бд и проверка наличия почты там
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('signup.html',
                                   form=form,
                                   message="Такой пользователь уже есть", teacher=teacher)
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            card_id=form.card_id.data,
            coins=500,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)  # добавление в бд
        db_sess.commit()
        return redirect('/login')
    return render_template('signup.html', form=form)


@app.route('/whoid')
def whoid_auth():
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    token = str(uuid.uuid4())
    return render_template('whoid.html', token=token, teacher=teacher)


@app.route('/log')
def log():
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    result = request.args.get('status')
    mail = request.args.get('mail')
    if result == "Success":
        return render_template('index.html', result=result, teacher=teacher)
    else:
        token = str(uuid.uuid4())
        return render_template('index.html', result=result, token=token, teacher=teacher)


@app.route('/forgot-password', methods=["POST", "GET"])
def forgotten_password_page():  # восстановление пароля
    if request.method == 'POST':
        '''
        login = gmail
        password = gmail_key  # отправка письма через сервера google
        server = smtplib.SMTP('smtp.gmail.com', 25)
        server.starttls()
        server.login(login, password)
        msg = MIMEMultipart()
        addr_to = request.form.get('email')
        msg['From'] = login
        msg['To'] = addr_to
        msg['Subject'] = 'Восстановление пароля'
        db_sess = db_session.create_session()
        all_emails = map(lambda x: x.email, db_sess.query(User).all())
        if addr_to in all_emails:
            # отправка идет на почту, указанную в форме: внутри письма ссылка для создания нового пароля
            client = db_sess.query(User).filter(User.email == addr_to).first()
            body = f"{client.name.capitalize()}, вот ваша ссылка для восстановления пароля:http://gametrade.pythonanywhere.com/reset_password?email={addr_to}&id={client.hashed_password}"
            msg.attach(MIMEText(body, 'plain'))
            server.send_message(msg)
            server.quit()  # письмо отправлено
            return redirect('/')  # есть letter.html но мне он показался не нужным
            '''
    return render_template('password_reset.html')


@app.route('/reset_password', methods=["POST", "GET"])
def reset_password():  # страница создания нового пароля
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    form = ResetPasswordForm()  # test http://127.0.0.1:5000/reset_password?email=fedotovk24@sch57.ru&id=1
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('new_password.html',
                                   form=form,
                                   message="Пароли не совпадают",
                                   teacher=teacher)
        else:
            print('Passwords are equal')
            client = request.args.get('email')
            url_client_id = request.args.get('id')  # сравнение параметров переданных в запросе с бд
            db_sess = db_session.create_session()
            if str(url_client_id) == \
                    str(db_sess.query(User.hashed_password).filter(User.email == client).first()[0]):
                print('DB client exists')
                client_account = db_sess.query(User).filter(User.email == client).first()
                client_account.set_password(form.password.data)
                db_sess.commit()  # смена пароля пользователя
                return redirect('/login')
    return render_template('new_password.html', form=form,
                           teacher=teacher)


@app.route('/rewards', methods=["GET", "POST"])
def show_items():  # каталог
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    db_sess = db_session.create_session()
    # начало работы с фильтрами и сортировкой
    data = db_sess.query(Item).order_by(Item.price).all()
    selected_sort = 'ascend'
    finder_value = ''
    if request.method == 'POST':
        name = request.form.get('need')
        if request.form.get('btn_finder') or name:  # работа фильтра  по названию
            data_find = []
            for product in data:
                if name.lower() in product.name.lower():
                    data_find.append(product)
            data = data_find
            finder_value = name
        if request.form.get('sorter') == 'descending':  # работа сортировки
            data = data[::-1]
            selected_sort = 'descending'
        else:
            data = data
            selected_sort = 'ascend'
        if request.form.get('btn'):
            item = db_sess.query(Item).filter(Item.id == int(request.form.get('btn'))).first()
            return redirect(f'/get_payment/?item_id={item.id}')
        return render_template('awards.html', logged=current_user.is_authenticated, data=data,
                               selected_sort=selected_sort, finder_value=finder_value,
                               teacher=teacher)
    return render_template('awards.html', logged=current_user.is_authenticated, data=data,
                           selected_sort=selected_sort, finder_value=finder_value,
                           teacher=teacher)


@app.route('/tasks', methods=["GET", "POST"])
def show_tasks():  # каталог
    user = load_user(current_user)
    db_sess = db_session.create_session()
    if user != None:
        teacher = user.check_teacher()
        data = db_sess.query(Task).filter(Task.grade == user.grade).all()
    else:
        teacher = False
        data = db_sess.query(Task).all()
    # начало работы с фильтрами и сортировкой
    selected_sort = 'ascend'
    finder_value = ''
    if request.method == 'POST':
        name = request.form.get('need')
        if request.form.get('btn_finder') or name:  # работа фильтра  по названию
            data_find = []
            for product in data:
                if name.lower() in product.name.lower():
                    data_find.append(product)
            data = data_find
            finder_value = name
        if request.form.get('sorter') == 'descending':  # работа сортировки
            data = data[::-1]
            selected_sort = 'descending'
        else:
            data = data
            selected_sort = 'ascend'
        if request.form.get('btn'):
            item = db_sess.query(Item).filter(Item.id == int(request.form.get('btn'))).first()
            return redirect(f'/get_payment/?item_id={item.id}')
        return render_template('tasks.html', logged=current_user.is_authenticated, data=data,
                               selected_sort=selected_sort, finder_value=finder_value,
                               teacher=teacher)
    return render_template('tasks.html', logged=current_user.is_authenticated, data=data,
                           selected_sort=selected_sort, finder_value=finder_value,
                           teacher=teacher)


@app.route('/profile', methods=["GET", "POST"])
@login_required
def show_profile():  # страница истории заказов
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    db_sess = db_session.create_session()
    orders = db_sess.query(Item).all()
    client_orders = []
    for order in orders:
        if int(order.client_id) == int(current_user.id):
            client_orders.append(order)
    return render_template('profile.html', orders=client_orders, user=current_user,
                           teacher=teacher)


@app.route('/recieve_payment', methods=["GET", "POST"])
def get_payment():  # получение оплаты, выдача товара
    db_sess = db_session.create_session()
    item = db_sess.query(Item).filter(Item.id == int(request.args.get('item_id'))).first().get_key()
    order = Transaction(
        time_transaction=datetime.datetime.now(),
        coin_change=int(item.price),
        user_id=int(current_user.get_id()),
        comment=item.description,
        item_id=int(item.id)
    )
    db_sess.add(order)
    db_sess.commit()


@app.errorhandler(404)  # обработка 404
def handle_error404(error):
    user = load_user(current_user)
    if user != None:
        teacher = user.check_teacher()
    else:
        teacher = False
    return render_template('404.html', logged=current_user.is_authenticated,
                           teacher=teacher)


@app.route('/letter')
def check_letter():
    return render_template('passwordprev.html')


@app.route('/greeting')
def check_greeting():
    return render_template('greeting.html')


def main():
    db_session.global_init("db/database.db")
    app.run(host='0.0.0.0', port=8090)


if __name__ == '__main__':
    main()
