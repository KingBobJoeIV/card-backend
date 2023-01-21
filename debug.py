from set_env import setup_env

setup_env()
# pylint: disable=unused-wildcard-import
from app.main import *
from app.db import db
from app.db.schemas import *
from app.models.user import *


def reset_db():
    User.__table__.drop(db.engine)
    Transaction.__table__.drop(db.engine)
    PhysicalCard.__table__.drop(db.engine)
    VirtualCard.__table__.drop(db.engine)
    db.create_all()


app.app_context().push()
