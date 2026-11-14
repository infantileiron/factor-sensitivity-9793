from sqlalchemy import String,Text,JSON,ForeignKey,Double,BigInteger
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class FactorMetric(RecordMixin,Base):
 __tablename__="factor_metrics"
 run_id:Mapped[str]=mapped_column(ForeignKey("runs.id"))
 factor_id:Mapped[str]=mapped_column(String(32))
 mu:Mapped[float]=mapped_column(Double)
 mu_star:Mapped[float]=mapped_column(Double)
 sigma:Mapped[float]=mapped_column(Double)
 s1:Mapped[float]=mapped_column(Double)
 st:Mapped[float]=mapped_column(Double)
 gap:Mapped[float]=mapped_column(Double)
 effect_count:Mapped[int]
 sigma_denominator:Mapped[int]
