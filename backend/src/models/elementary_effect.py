from sqlalchemy import String,Text,JSON,ForeignKey,Double,BigInteger
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class ElementaryEffect(RecordMixin,Base):
 __tablename__="elementary_effects"
 run_id:Mapped[str]=mapped_column(ForeignKey("runs.id"))
 trajectory:Mapped[int]
 factor_id:Mapped[str]=mapped_column(String(32))
 signed_step:Mapped[float]=mapped_column(Double)
 effect:Mapped[float]=mapped_column(Double)
