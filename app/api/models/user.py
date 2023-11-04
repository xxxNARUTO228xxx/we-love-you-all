from models import Base
from sqlalchemy import Column, Text, UniqueConstraint
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import relationship

from models.analyzer_model import ModelReport


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = 'user'

    name = Column(Text, nullable=False)

    model_reports = relationship('ModelReport', foreign_keys='[ModelReport.user_id]',
                                 back_populates='user')

    __table_args__ = (
        UniqueConstraint('email', name='user_email_constraint'),
        {'schema': 'auth'}
    )