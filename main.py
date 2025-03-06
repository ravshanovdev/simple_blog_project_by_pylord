from pylord.orm import Database
from models import Blog, Category
from pylord.app import PyLordApp

app = PyLordApp()


@app.route("/create_category", allowed_methods=['post'])
def create_category(req, resp):
    db = Database("./blogapp.db")
    db.create(Category)

    category = Category(**req.POST)
    db.save(category)

    resp.status_code = 201
    resp.json = {'name': category.name}


@app.route("/get_category", allowed_methods=["get"])
def get_category(req, resp):
    db = Database("./blogapp.db")

    category = db.all(Category)

    resp.status_code = 200
    resp.json = [{"id": cat.id, "name": cat.name} for cat in category]
