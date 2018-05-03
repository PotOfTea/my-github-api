from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import BIGINT, TEXT, UUID, ARRAY
from sqlalchemy.sql.expression import text
from database import db
import json

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
