from pylord.app import PyLordApp
import handlers
import models
from waitress import serve

app = PyLordApp(__name__)

for handler_app in handlers.apps:
    for path, handler_data in handler_app.routes.items():
        app.add_route(path, handler_data["handler"], handler_data["allowed_methods"])

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
