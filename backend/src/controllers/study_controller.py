from sqlalchemy import select
from ..models.study import SensitivityStudy
from ..models.common import serialize
from ..services import study_service as service
from .common import require
def list_all(db):return [serialize(row) for row in db.scalars(select(SensitivityStudy).order_by(SensitivityStudy.created_at.desc())).all()]
def detail(db,ident):
 row=require(db,SensitivityStudy,ident)
 return serialize(row)
def create(db,body):
 row=service.create(db,body)
 return serialize(row)
