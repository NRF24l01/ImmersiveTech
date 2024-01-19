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
