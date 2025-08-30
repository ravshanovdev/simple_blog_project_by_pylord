from pylord.app import PyLordApp
from models.models import User
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from .secret_keys import generate_token

app = PyLordApp()


def hash_password(password):
    return generate_password_hash(password)


def check_password(password, hashed_password):
    return check_password_hash(hashed_password, password)


@app.route("/user_register", allowed_methods=['post'])
def user_register(req, resp):
    db = get_db()
    db.create(User)
    data = req.json
    username = data.get("username")
    email = data.get("email")
    password1 = data.get("password1")
    password2 = data.get("password2")

    if not username or not email or not password1 or not password2:
        resp.status_code = 400
        resp.json = {"error": "qatorlarni toldiring"}

    if password1 != password2:
        resp.status_code = 400
        resp.json = {"error": "password mos emas"}

    # existing_user = db.conn.execute("SELECT id FROM user WHERE username = ? OR email = ?", (username, email)).fetchone()

    existing_user = db.get_user(User, field_name='username', value=username)
    existing_email = db.get_user(User, field_name='email', value=email)

    if existing_user:
        resp.status_code = 400
        resp.json = {"error": "user already exist"}
        return
    elif existing_email:
        resp.status_code = 400
        resp.json = {"error": "Email already exist"}
        return
    else:
        hashed_password = hash_password(data["password1"])

        db.save(
            User(
                username=username,
                email=email,
                password_hash=hashed_password
            )
        )

        resp.status_code = 201
        resp.json = {
            "username": username,
            "email": email,
            "password1": password1,
            "password2": password2
        }


@app.route("/login", allowed_methods=['post'])
def login(req, resp):
    db = get_db()

    data = req.json
    username = data.get("username")
    password = data.get("password1")

    if not username or not password:
        resp.status_code = 400
        resp.json = {"message": "Username va password kiritish shart!"}

    user = db.conn.execute("SELECT id, password_hash FROM user WHERE username = ?", (username,)).fetchone()
    # user = db.get_by_field(User, field_name='username', value=username)

    if not user or not check_password(password, user[1]):
        resp.status_code = 401
        resp.json = {"error": "Noto‘g‘ri username yoki parol!"}

    token = generate_token(user[0], username=username)

    resp.status_code = 200
    resp.json = {"token": token}
