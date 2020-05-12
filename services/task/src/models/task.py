from src import db
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    def __init__(self,description):
        self.description = description
        # self.created_at = created_at

    def __repr__(self):
        return "# task ID:{}  description - {} date {}".format(self.id,self.description,self.created_at)

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'created_at': self.created_at.strftime("%m/%d/%Y"),
        }

    def save(self, commit=True):
        """ save """
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, payload, commit=True):
        """ update """
        for attr, value in payload.items():
            setattr(self, attr, value)
        return commit and self.save() or self
    
