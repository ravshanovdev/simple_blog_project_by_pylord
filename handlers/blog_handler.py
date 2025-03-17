from database import get_db
from models.models import Blog, Category
from pylord.app import PyLordApp
from .category_handler import update_handler
from .secret_keys import auth_required
app = PyLordApp()


@app.route("/create_blog", allowed_methods=['post'])
@auth_required
def create_blog(req, resp):
    db = get_db()
    db.create(Blog)
    data = req.json

    try:
        category = db.get(Category, data["category_id"])

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
    except Exception as e:
        resp.status_code = 500
        resp.json = {"error": str(e)}


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
def updateblog(req, resp, id):
    update_handler(req, resp, Blog, id=id)

    # update_handler() dan ham foydalanish mumkin yoki uzingiz qo'lda shunday yozishingiz ham mumkin
    # db = get_db()
    # blog = db.get(Blog, id=id)
    #
    # if not blog:
    #     resp.status_code = 404
    #     resp.json = {"message": "blog not found"}
    #     return
    #
    # try:
    #     required_fields = ["name", "description", "about"]
    #     for field in required_fields:
    #         if field not in req.json:
    #             resp.status_code = 400
    #             resp.json = {"error": f"'{field}' field is required"}
    #             return
    #
    #     blog.name = req.json["name"]
    #     blog.description = req.json["description"]
    #     blog.about = req.json["about"]
    #
    #
    #     category = db.get(Category, id=req.json["category"])
    #     if not category:
    #          resp.status_code = 404
    #          resp.json = {"error": "category not found"}
    #          return
    #     blog.category = category
    #
    #     db.update(blog)
    #     resp.status_code = 200
    #     resp.json = {"message": "object was successfully updated"}
    #
    # except Exception as e:
    #     resp.status_code = 500
    #     resp.json = {"error": str(e)}


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

