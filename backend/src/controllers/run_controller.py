from sqlalchemy import select
from ..models.run import SensitivityRun
from ..models.common import serialize
from ..services import run_service as service
from .common import require
def list_all(db):return [serialize(row) for row in db.scalars(select(SensitivityRun).order_by(SensitivityRun.created_at.desc())).all()]
def detail(db,ident):
 row=require(db,SensitivityRun,ident)
 return serialize(row)
def create(db,body):
 row=service.create(db,body)
 return serialize(row)
