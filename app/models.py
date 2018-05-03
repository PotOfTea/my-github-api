from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, UUID, ARRAY
from sqlalchemy.sql.expression import text
from database import db
import json

#http://blog.mmast.net/sqlalchemy-serialize-json

class User(db.Model):
    __tablename__ = 'user'

    #id = Column(BIGINT, primary_key=True,autoincrement=True, nullable=False)
    username = Column(String(32), nullable=False)
    uuid = Column(UUID, primary_key=True, server_default=text('uuid_generate_v1mc()'))
    games_played = Column(BIGINT, nullable=False, default=0)
    score = Column(BIGINT, nullable=False, default=0)
    friends = Column(ARRAY(UUID, dimensions=1), default=[])

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<username {}'.format(self.username)

    def as_json(self):
        return json.dumps({c.name: getattr(self, c.name) for c in self.__table__.columns})


class Github(db.Model):
    __tablename__ = 'github'

    id = Column(BIGINT,primary_key=True, nullable=False)
    name = Column(String(150), nullable=False)
    full_name = Column(String(350), nullable=False)
    html_url = Column(String(350), nullable=False)
    language = Column(String(150), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=False, index=True)
    pushed_at = Column(DateTime(timezone=True), nullable=False)
    stargazers_count = Column(BIGINT, default=0, nullable=False, index=True)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<full_name {}'.format(self.full_name)

    def as_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}