from .category_handler import app as category_app
from .blog_handler import app as blog_app
from .register import app as user_app

apps = [category_app, blog_app, user_app]

