from flask import current_app, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker


Base = declarative_base()


def get_engine():
    if 'db_engine' not in g:
        g.db_engine = create_engine(current_app.config['DATABASE'], convert_unicode=True)
    return g.db_engine


def get_session():
    if 'db_session' not in g:
        db_engine = get_engine()
        g.db_session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=db_engine))
    return g.db_session


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
