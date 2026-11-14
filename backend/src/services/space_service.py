from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.space import FactorSpace
from ..models.response_model import ResponseModel
from ..models.factor_range import FactorRange
from ..models.common import serialize
from .model_service import specification
from .polynomial import validate_ranges
from .csv_data import records
def ranges(db,row):return [{k:getattr(f,k) for k in ['factor_id','low','high']} for f in db.scalars(select(FactorRange).where(FactorRange.space_id==row.id)).all()]
def expanded(db,row):return {**serialize(row),'ranges':ranges(db,row)}
def create(db,body):
 model=db.get(ResponseModel,body.model_id)
 if not model:raise HTTPException(422,'代理模型不存在')
 try:rows=validate_ranges(specification(db,model),records(body.ranges_csv,['factor_id','low','high'],6))
 except ValueError as error:raise HTTPException(422,str(error))
 if db.scalar(select(FactorSpace).where(FactorSpace.name==body.name)):raise HTTPException(409,'因子空间名称已存在')
 row=FactorSpace(id=str(uuid4()),name=body.name,model_id=model.id,description=body.description);db.add(row);db.flush()
 for f in rows:db.add(FactorRange(id=str(uuid4()),space_id=row.id,**f))
 db.commit();return row
