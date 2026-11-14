from sqlalchemy import String,Text,JSON,ForeignKey,Double,BigInteger
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class ModelInteraction(RecordMixin,Base):
 __tablename__="model_interactions"
 model_id:Mapped[str]=mapped_column(ForeignKey("response_models.id"))
 left:Mapped[str]=mapped_column(String(32))
 right:Mapped[str]=mapped_column(String(32))
 coefficient:Mapped[float]=mapped_column(Double)
