from sqlalchemy import select
from ..models.review import FactorReview
from ..models.common import serialize
from ..services import review_service as service
from .common import require
def list_all(db):return [serialize(row) for row in db.scalars(select(FactorReview).order_by(FactorReview.created_at.desc())).all()]
def detail(db,ident):
 row=require(db,FactorReview,ident)
 return serialize(row)
def create(db,body):
 row=service.create(db,body)
 return serialize(row)
def approve(db,ident,user):return serialize(service.approve(db,require(db,FactorReview,ident),user))
