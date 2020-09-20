from sqlalchemy import Column, Integer, String, Binary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UrlsTab(Base):
    __tablename__ = 'urls_tab'

    id = Column(Integer, primary_key=True)
    url = Column(String(2083))
    short_key = Column(String(32))
    hashed_url = Column(Binary(20))
    ctime = Column(Integer)
