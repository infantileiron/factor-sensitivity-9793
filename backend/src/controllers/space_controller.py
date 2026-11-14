from sqlalchemy import select
from ..models.space import FactorSpace
from ..models.common import serialize
from ..services import space_service as service
from .common import require
def list_all(db):return [service.expanded(db,row) for row in db.scalars(select(FactorSpace).order_by(FactorSpace.created_at.desc())).all()]
def detail(db,ident):
 row=require(db,FactorSpace,ident)
 return service.expanded(db,row)
def create(db,body):
 row=service.create(db,body)
 return service.expanded(db,row)
