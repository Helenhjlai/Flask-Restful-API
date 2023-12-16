from restdemo import db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from restdemo.model.base import Base


class Tweet(Base):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    body = db.Column(db.String(140))
    create_at = db.Column(db.DateTime, server_default=func.now(), default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "user_id = {}, tweet = {}".format(self.user_id, self.body)

    def as_dict(self):
        t = {t.name: getattr(self, t.name) for t in self.__table__.columns}
        t['create_at'] = t['create_at'].isoformat()
        return t
