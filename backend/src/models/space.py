from sqlalchemy import String,Text,JSON,ForeignKey,Double,BigInteger
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class FactorSpace(RecordMixin,Base):
 __tablename__="spaces"
 name:Mapped[str]=mapped_column(String(180),unique=True)
 model_id:Mapped[str]=mapped_column(ForeignKey("response_models.id"))
 description:Mapped[str]=mapped_column(Text,default="")
