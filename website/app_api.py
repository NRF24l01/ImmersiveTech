import os.path
import pathlib
import flask
from flask import jsonify, request
from data import db_session
from data.work_with_db import Item, User, Transaction

blueprint = flask.Blueprint(
    'game_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/register', methods=['POST', 'GET'])
def register_user():
        try:
            db_sess = db_session.create_session()
            user = User(
                name=request.args.get('name'),
                surname=request.args.get('surname'),
                card_id=request.args.get('card_id'),
                coins=500,
                email=request.args.get('email')
            )
            user.set_password(request.args.get('password'))
            db_sess.add(user)  #
            db_sess.commit()
            return jsonify({'SUCCESS': 'User has been registered!'})
        except Exception:
            return jsonify({'ERROR': 'Error while registering user!'})


@blueprint.route('/api/get_data', methods=['POST', 'GET'])
def student_data():
        try:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.card_id == request.form.get('card_id')).first()
            orders = db_sess.query(Item).all()
            client_orders = []
            for order in orders:
                if int(order.client_id) == int(user.id):
                    trsc = {"id": order.id,
                            "coin_change": order.coin_change,
                            "comment": order.comment,
                            "time": order.transaction_time,
                            "item_id": order.item_id}
                    client_orders.append(trsc)
            return jsonify({"coins": user.coins, "transactions": client_orders})
        except Exception:
            return jsonify({'ERROR': 'Error while getting data!'})
