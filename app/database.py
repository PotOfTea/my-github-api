from sqlite3 import IntegrityError

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import database_exists, create_database

db = SQLAlchemy()
Base = declarative_base()

def init_db_if_exist():
    engine = db.engine
    print("Configuring db")
    if not database_exists(engine.url):
        print("DB doesn't exist, creating")
        create_database(engine.url)
    else:
        current_app.logger.info("DB exist, skipping...")

    if not schema_exists(engine, "user") or not schema_exists(engine, "github"):
        from models import User, Github
        db.drop_all()
        db.create_all()
    else:
        current_app.logger.info("Table exist, skipping...")
    engine.dispose()


def init_db_if_exist_foo():
    engine = db.engine
    current_app.logger.info("Configuring db")
    if not database_exists(engine.url):
        current_app.logger.info("DB doesn't exist, creating")
        create_database(engine.url)
    else:
        current_app.logger.info("DB exist, skipping...")

    print("Creating db schemas ....")


    # if not engine.dialect.has_table(engine, "user", "public"):
    #     current_app.logger.info("Table doesn't exist, creating")
    #     from models import User
    #     db.drop_all()
    #     db.create_all()
    # else:
    #     current_app.logger.info("Table exist, skipping...")
    #
    if not schema_exists(engine):
        print("Table doesn't exist, creating")
        from models import Github

        schema_exists(engine)
        #db.create_all()
        get_one_or_create(db.session, Github)
        schema_exists(engine)

    else:
        print("Table exist, skipping...")

    engine.dispose()

def get_one_or_create(session,
                      model,
                      create_method='',
                      create_method_kwargs=None,
                      **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), False
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, True
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), False


def schema_exists(engine, table):
    schema_status = engine.dialect.has_table(engine, table, "public")
    print("table: '"+table+"' exists: "+str(schema_status))
    return schema_status
