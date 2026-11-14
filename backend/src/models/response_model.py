from sqlalchemy import String,Text,JSON,ForeignKey,Double,BigInteger
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class ResponseModel(RecordMixin,Base):
 __tablename__="response_models"
 name:Mapped[str]=mapped_column(String(180),unique=True)
 description:Mapped[str]=mapped_column(Text,default="")
 intercept:Mapped[float]=mapped_column(Double)
 response_unit:Mapped[str]=mapped_column(String(20),default="kWh")
