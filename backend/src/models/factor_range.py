from sqlalchemy import String,Text,JSON,ForeignKey,Double,BigInteger
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class FactorRange(RecordMixin,Base):
 __tablename__="factor_ranges"
 space_id:Mapped[str]=mapped_column(ForeignKey("spaces.id"))
 factor_id:Mapped[str]=mapped_column(String(32))
 low:Mapped[float]=mapped_column(Double)
 high:Mapped[float]=mapped_column(Double)
