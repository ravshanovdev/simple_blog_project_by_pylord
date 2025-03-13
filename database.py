from pylord.orm import Database
import threading

thread_local = threading.local()


def get_db():
    if not hasattr(thread_local, "db"):
        thread_local.db = Database("./blogapp.db")
    return thread_local.db
