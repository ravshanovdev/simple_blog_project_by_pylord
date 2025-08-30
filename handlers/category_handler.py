from models.models import Category
from pylord.app import PyLordApp
from database import get_db
from .secret_keys import auth_required
from .dynamic_handlers import update_handler
app = PyLordApp()


@app.route("/create_category", allowed_methods=['post'])
@auth_required
def create_category(req, resp):
    db = get_db()
    db.create(Category)
    category = Category(**req.POST)
    db.save(category)

    resp.status_code = 201
    resp.json = {'name': category.name}


@app.route("/get_all_category", allowed_methods=["get"])
def get_category(req, resp):
    db = get_db()
    category = db.all(Category)

    resp.status_code = 200
    resp.json = [{"id": cat.id, "name": cat.name} for cat in category]


@app.route("/get_category/{id:d}", allowed_methods=["get"])
def get_category_by_id(req, resp, id):
    db = get_db()

    try:
        category = db.get(Category, id=id)

        resp.status_code = 200
        resp.json = {"id": category.id, "name": category.name}

    except Exception as e:
        resp.status_code = 404
        resp.json = {"message": [str(e)]}


@app.route("/delete_category/{id:d}", allowed_methods=["delete"])
def delete_category_by_id(req, resp, id):
    db = get_db()

    try:
        category_id = db.get(Category, id)
        if category_id:
            db.delete(Category, id)

            resp.status_code = 200
            resp.json = {"message": "Category Was Successfully Deleted"}

    except Exception as e:
        resp.status_code = 401
        resp.json = {"message": [str(e)]}


@app.route("/update_category/{id:d}", allowed_methods=['patch'])
def update_category_by_id(req, resp, id):
    update_handler(req, resp, Category, id)
