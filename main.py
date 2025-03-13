from pylord.orm import Database
from models import Blog, Category, Author, Book
from pylord.app import PyLordApp
import threading

thread_local = threading.local()
app = PyLordApp()


def get_db():
    if not hasattr(thread_local, "db"):
        thread_local.db = Database("./blogapp.db")
    return thread_local.db


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


# BLOG part

@app.route("/create_blog", allowed_methods=['post'])
def create_blog(req, resp):
    db = get_db()
    db.create(Blog)
    data = req.json

    category = db.get(Category, data["category_id"])

    if not category:
        resp.status_code = 404
        resp.json = {"error": "Category not found"}
        return

    blog = Blog(
        name=data["name"],
        description=data["description"],
        about=data["about"],
        category=category,
    )

    db.save(blog)

    resp.status_code = 201
    resp.json = {"id": blog.id, "category_name": category.name,
                 "name": blog.name, "description": blog.description,
                 "about": blog.about
                 }


@app.route("/get_all_blog", allowed_methods=['get'])
def get_all_blogs(req, resp):
    db = get_db()

    blogs = db.all(Blog)

    if not blogs:
        resp.status_code = 404
        resp.json = {"message": "Blog Not Found"}
        return

    resp.status_code = 200
    resp.json = [{
        "id": blog.id,
        "name": blog.name,
        "category": [blog.category.id, blog.category.name] if blog.category else None,
        "description": blog.description,
        "about": blog.about
    } for blog in blogs]

