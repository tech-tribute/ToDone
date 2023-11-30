from todone import db
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import datetime


class Task(db.Model):
    __tablename__ = "tasks"
    id = Column(Integer(), nullable=False, primary_key=True)
    caption = Column(String(128), nullable=False)
    create = Column(DateTime(), default=datetime.now, nullable=False)
    done = Column(Boolean(), nullable=False, default=False)

    def is_caption(self, caption):
        return len(caption) > 3
