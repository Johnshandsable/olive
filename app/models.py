from datetime import datetime
from app import db, ma
from flask_marshmallow import Marshmallow


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    family_size = db.Column(db.Integer, nullable=False)
    family_name = db.Column(db.String, nullable=False)
    check_in = db.relationship('CheckIn', backref='user.id', lazy='dynamic')

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
    organization = db.Column(db.String, default="")
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

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


class UserSchema(ma.ModelSchema):
    class Meta():
        fields = ('id', 'family_size', 'family_name')


class CheckInSchema(ma.ModelSchema):
    class Meta():
        fields = ('organization', 'timestamp', 'user_id')
