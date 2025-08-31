from database import get_db
from models.models import Blog, Category, User
from pylord.app import PyLordApp
from .dynamic_handlers import update_handler
from .secret_keys import auth_required
app = PyLordApp()


@app.route("/create_blog", allowed_methods=['post'])
@auth_required
def create_blog(req, resp):
    db = get_db()
    db.create(Blog)
    data = req.json
    user = db.get(User, id=req.user_id)
    try:
        category = db.get(Category, data["category_id"])

        blog = Blog(
            user=user,
            name=data["name"],
            description=data["description"],
            about=data["about"],
            category=category,
        )

        db.save(blog)

        resp.status_code = 201
        resp.json = {"id": blog.id, "user_id": blog.user.username, "category_name": category.name,
                     "name": blog.name, "description": blog.description,
                     "about": blog.about
                     }
    except Exception as e:
        resp.status_code = 500
        resp.json = {"error": str(e)}


@app.route("/get_all_blog", allowed_methods=['get'])
def get_all_blogs(req, resp):
    db = get_db()

    blogs = db.all(Blog)

    if not blogs:
        resp.status_code = 404
        resp.json = {"message": "Not Any Blogs Found"}
        return

    resp.status_code = 200
    resp.json = [{
        "id": blog.id,
        "user": blog.user.username,
        "name": blog.name,
        "category": [blog.category.id, blog.category.name] if blog.category else None,
        "description": blog.description,
        "about": blog.about
    } for blog in blogs]


class GetBlogById:

    def get(self, req, resp, id):
        db = get_db()

        try:
            blog = db.get(Blog, id=id)

            resp.status_code = 200
            resp.json = {
                "id": blog.id,
                "name": blog.name,
                "category": blog.category.name,
                "description": blog.description,
                "about": blog.about
            }

        except Exception as e:
            resp.status_code = 404
            resp.json = {"error": str(e)}


app.add_route("/get_blog/{id:d}", GetBlogById, allowed_methods=['get'])


@app.route("/update_blog/{id:d}", allowed_methods=['patch'])
@auth_required
def updateblog(req, resp, id):
    update_handler(req, resp, Blog, id=id)


@app.route("/delete_blog/{id:d}", allowed_methods=['delete'])
def delete_blog(req, resp, id):
    db = get_db()

    try:
        blog = db.get(Blog, id=id)
        if blog:
            db.delete(Blog, id=id)

            resp.status_code = 200
            resp.json = {"message": "Blog Was Successfully Delete"}
    except Exception as e:
        resp.status_code = 404
        resp.json = {"error": str(e)}


@app.route("/get_blog_by_name/{names}", allowed_methods=['get'])
def get_blog_by_name(req, resp, names: str):
    db = get_db()

    try:

        blog = db.get_by_field(Blog, field_name='name', value=names)

        resp.status_code = 200
        resp.json = {
            "id": blog.id,
            "name": blog.name,
            "description": blog.description,
            "category": blog.category.name
        }

    except Exception as e:
        resp.status_code = 404
        resp.json = {"error": str(e)}

