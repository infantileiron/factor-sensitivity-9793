from sqlalchemy import String,Text,JSON,ForeignKey,Double,BigInteger
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class ModelFactor(RecordMixin,Base):
 __tablename__="model_factors"
 model_id:Mapped[str]=mapped_column(ForeignKey("response_models.id"))
 factor_id:Mapped[str]=mapped_column(String(32))
 name:Mapped[str]=mapped_column(String(80))
 unit:Mapped[str]=mapped_column(String(30))
 linear:Mapped[float]=mapped_column(Double)
 quadratic:Mapped[float]=mapped_column(Double)
