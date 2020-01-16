from flask import jsonify
from app import app, db
from app.models import User, CheckIn, UserSchema, CheckInSchema
from app.funcs import get_query

"""

user_schema = UserSchema()
output = user_schema.dump(user).data
return jsonify({'user': output})
"""

def func():
    try:
        users = User.query.all()
        user_schema = UserSchema(many=True)
        output = user_schema.dump(users)
        return jsonify({'output': output})
    except AttributeError as error:
        print(error)

def test_1():
    get_query(month='All', organization='Master', year=2019)
    get_query.filter_by(user_id)


if __name__ == "__main__":
    test_1()
