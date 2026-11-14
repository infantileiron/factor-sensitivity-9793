from sqlalchemy import String,Text,JSON,ForeignKey,Double,BigInteger
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class EvaluationPoint(RecordMixin,Base):
 __tablename__="evaluation_points"
 run_id:Mapped[str]=mapped_column(ForeignKey("runs.id"))
 trajectory:Mapped[int]
 step:Mapped[int]
 normalized:Mapped[dict]=mapped_column(JSON)
 physical:Mapped[dict]=mapped_column(JSON)
 response:Mapped[float]=mapped_column(Double)
