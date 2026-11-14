from sqlalchemy import String,Text,JSON,ForeignKey,Double,BigInteger
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class SensitivityStudy(RecordMixin,Base):
 __tablename__="studies"
 name:Mapped[str]=mapped_column(String(180),unique=True)
 model_id:Mapped[str]=mapped_column(ForeignKey("response_models.id"))
 space_id:Mapped[str]=mapped_column(ForeignKey("spaces.id"))
 trajectories:Mapped[int]
 levels:Mapped[int]
 power:Mapped[int]
 seed:Mapped[int]=mapped_column(BigInteger)
