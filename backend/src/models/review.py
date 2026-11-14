from sqlalchemy import String,Text,JSON,ForeignKey,Double,BigInteger
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class FactorReview(RecordMixin,Base):
 __tablename__="reviews"
 run_id:Mapped[str]=mapped_column(ForeignKey("runs.id"))
 action:Mapped[str]=mapped_column(Text)
 state:Mapped[str]=mapped_column(String(20),default="submitted")
 reviewer:Mapped[str]=mapped_column(String(180),default="")
