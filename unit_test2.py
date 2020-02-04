from app import app, db, bcrypt
from app.models import User, UserLogin, CheckIn, UserSchema, CheckInSchema
from app.queries import get_query, write_query


def create_user():
    username = input("Enter username")
    password = input("Enter password")
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = UserLogin(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    print("Account created for: ", user)

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
    create_user()
