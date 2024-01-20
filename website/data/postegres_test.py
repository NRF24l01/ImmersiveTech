from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from website.app import app


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postegre_site:1DKar$odE*pmIQg%8RLo@192.168.115.201/school_bank'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
