from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from slugify import slugify


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    school = db.Column(db.String(128))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    mat1_tests = db.relationship('Mat1', backref='mat1', lazy='dynamic')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.username)


class Mat1(db.Model):

    __tablename__ = "mat1"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    teacher = db.Column(db.String(80))
    klasse = db.Column(db.String(200))
    beskrivelse = db.Column(db.Text(800))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    slug = db.Column(db.String(1000), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mat1_test = db.relationship('Mat1tests', backref='mat1s', lazy='dynamic')

    def __repr__(self):
        return '{}, {}'.format(id, self.title)

    @staticmethod
    def slugify (target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)


db.event.listen(Mat1.title, 'set', Mat1.slugify, retval=False)


class Mat1tests(db.Model):

    __tablename__ = "mat1tests"

    id = db.Column(db.Integer, primary_key=True)
    elev = db.Column(db.String(120))
    a1 = db.Column(db.Integer)
    b1 = db.Column(db.Integer)
    b2 = db.Column(db.Integer)
    c1 = db.Column(db.Integer)
    d1 = db.Column(db.Integer)
    d2 = db.Column(db.Integer)
    d3 = db.Column(db.Integer)
    d4 = db.Column(db.Integer)
    e1 = db.Column(db.Integer)
    mat1_sum = db.Column(db.Integer)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    comments = db.Column(db.Text(800))
    delete = db.Column(db.Boolean(), default=False)
    mat1_id = db.Column(db.Integer, db.ForeignKey('mat1.id'))
