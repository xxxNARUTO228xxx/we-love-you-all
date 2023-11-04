from models import Base
from sqlalchemy import Column, text, Text, sql, SmallInteger, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

from sqlalchemy_utils import JSONType
from sqlalchemy.orm import relationship


class ModelReport(Base):
    __tablename__ = 'model_report'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                server_default=text("gen_random_uuid()"))

    datetime = Column(DateTime(True), nullable=False, server_default=sql.func.now(),
                      default=datetime.datetime.utcnow)
    user_id = Column(UUID(as_uuid=False), ForeignKey('auth.user.id'), nullable=True)

    config = Column(JSONType, nullable=True)

    user = relationship('User', foreign_keys=[user_id], back_populates='model_reports')

    __table_args__ = (
        {'schema': 'analyzer_model'}
    )
