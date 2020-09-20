import atexit
import logging
import time
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from conf import Conf

engine = create_engine(**Conf['database'])
Session = sessionmaker(bind=engine)
sqlLogger = logging.getLogger('sql')


@contextmanager
def session_ctx(s=Session()):
    try:
        yield s
        s.flush()
        s.expunge_all()
        s.commit()
    except:
        s.rollback()
        raise
    finally:
        s.close()


@atexit.register
def close_pool():
    engine.dispose()


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    sqlLogger.debug('%.1f %s', total * 1000, statement)
