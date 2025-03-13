from .category_handler import get_db
from models.models import Blog, Category
from pylord.app import PyLordApp

app = PyLordApp()


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

