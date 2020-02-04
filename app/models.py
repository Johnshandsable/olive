from datetime import datetime
from app import db, ma, login_manager
from flask_login import UserMixin
from marshmallow import Schema, fields


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


@login_manager.user_loader
def load_user(user_id):
    return UserLogin.query.get(int(user_id))


class UserLogin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    @staticmethod
    def add_login(user):
        db.session.add(user)
        db.session.commit()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    family_size = db.Column(db.Integer, nullable=False)
    family_name = db.Column(db.String, nullable=False)
    check_in = db.relationship('CheckIn', backref='client', lazy='dynamic')

    def __repr__(self):
        return f"Client ID: {self.id}"

    @staticmethod
    def add_user(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def validate_new(new_user):
        query = User.query.filter_by(family_size=new_user.family_size,
                                     family_name=new_user.family_name).first()
        if query is None:
            return True  # returns True if the user may not already exist
        else:
            return False  # returns False if the user may already exist


class CheckIn(db.Model):
    __tablename__ = "checkins"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    organization = db.Column(db.String, default="")
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.user_id}, {self.organization}, {self.timestamp}"

    @staticmethod
    def checkin(checkin):
        db.session.add(checkin)
        db.session.commit()

    @staticmethod
    def validate_existing(ex_user):
        query = User.query.filter_by(id=ex_user.user_id).first()
        if query is not None:
            return True  # returns True if user already exists
        else:
            return False  # returns False if user does not already exist

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'user_id': self.user_id,
           'checked_in': dump_datetime(self.timestamp),
           'organization': self.organization}
           # 'many2many'  : self.serialize_many2many

    @property
    def serialize_many2many(self):
       """
       Return object's relations in easily serializable format.
       NB! Calls many2many's serialize property.
       """
       return [ item.serialize for item in self.many2many]

class UserSchema(Schema):
    id = fields.Int()
    date_created = fields.DateTime()
    family_size = fields.Str()
    family_name = fields.Str()


class CheckInSchema(Schema):
    user_id = fields.Int()
    organization = fields.Str()
    timestamp = fields.DateTime()
