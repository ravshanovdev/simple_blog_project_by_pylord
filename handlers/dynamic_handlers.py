from pylord.app import PyLordApp
from database import get_db
from pylord.orm import ForeignKey
app = PyLordApp()


def update_handler(req, resp, table, id):
    db = get_db()

    try:

        instance = db.get(table, id=id)
        if not instance:
            resp.status_code = 404
            resp.json = {"error": "Object not found"}
            return

        for key, value in req.json.items():
            if hasattr(instance, key):
                attr = getattr(table, key)
                if isinstance(attr, ForeignKey):

                    foreignkey_table = attr.table

                    related_instance = db.get(foreignkey_table, id=value)

                    if not related_instance:
                        resp.status_code = 404
                        resp.json = {"error": f"{key.__name__} object with id {value} not found"}
                        return

                    setattr(instance, key, related_instance)
                else:
                    setattr(instance, key, value)
            else:
                resp.status_code = 400
                resp.json = {"error": f"Invalid field: {key}"}
                return

        db.update(instance)

        resp.status_code = 200
        resp.json = {"message": "Updated successfully", "instance_id": instance.id}

    except Exception as e:
        resp.status_code = 500
        resp.json = {"error": str(e)}