from models.models import Category
from pylord.app import PyLordApp
from database import get_db

app = PyLordApp()


def update_handler(req, resp, table, id):
    db = get_db()

    try:
        # Ma'lumotlar bazasidan mavjud obyektni olish
        instance = db.get(table, id=id)

        # Yangi qiymatlarni yangilash
        for key, value in req.json.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
            else:
                resp.status_code = 400
                resp.json = {"error": f"Invalid field: {key}"}
                return

        # O'zgarishlarni saqlash
        db.update(instance)

        resp.status_code = 200
        resp.json = {"message": "Updated successfully", "instance_id": instance.id, "instance_name": instance.name}

    except Exception as e:
        resp.status_code = 500
        resp.json = {"error": str(e)}


@app.route("/create_category", allowed_methods=['post'])
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
            del_category = db.delete(Category, id)

            resp.status_code = 200
            resp.json = {"message": "Category Was Successfully Deleted"}

    except Exception as e:
        resp.status_code = 401
        resp.json = {"message": [str(e)]}


@app.route("/update_category/{id:d}", allowed_methods=['patch'])
def update_category_by_id(req, resp, id):
    update_handler(req, resp, Category, id)
