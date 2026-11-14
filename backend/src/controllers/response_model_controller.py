from sqlalchemy import select
from ..models.response_model import ResponseModel
from ..models.common import serialize
from ..services import model_service as service
from .common import require
def list_all(db):return [service.expanded(db,row) for row in db.scalars(select(ResponseModel).order_by(ResponseModel.created_at.desc())).all()]
def detail(db,ident):
 row=require(db,ResponseModel,ident)
 return service.expanded(db,row)
def create(db,body):
 row=service.create(db,body)
 return service.expanded(db,row)
def patch(db,ident,body):
 row=require(db,ResponseModel,ident);row.description=body.description;db.commit();return service.expanded(db,row)
