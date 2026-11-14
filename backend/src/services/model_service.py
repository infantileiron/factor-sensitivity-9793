from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.response_model import ResponseModel
from ..models.model_factor import ModelFactor
from ..models.model_interaction import ModelInteraction
from ..models.common import serialize
from .polynomial import validate_model
from .csv_data import records
def specification(db,row):
 return {'intercept':row.intercept,'response_unit':row.response_unit,'factors':[{k:getattr(f,k) for k in ['factor_id','name','unit','linear','quadratic']} for f in db.scalars(select(ModelFactor).where(ModelFactor.model_id==row.id).order_by(ModelFactor.created_at,ModelFactor.id)).all()],'interactions':[{k:getattr(f,k) for k in ['left','right','coefficient']} for f in db.scalars(select(ModelInteraction).where(ModelInteraction.model_id==row.id).order_by(ModelInteraction.id)).all()]}
def expanded(db,row):return {**serialize(row),**specification(db,row)}
def create(db,body):
 try:
  model=validate_model({'intercept':body.intercept,'factors':records(body.factors_csv,['factor_id','name','unit','linear','quadratic'],6),'interactions':records(body.interactions_csv,['left','right','coefficient'],15)})
 except ValueError as error:raise HTTPException(422,str(error))
 if db.scalar(select(ResponseModel).where(ResponseModel.name==body.name)):raise HTTPException(409,'模型名称已存在')
 row=ResponseModel(id=str(uuid4()),name=body.name,description=body.description,intercept=model['intercept'],response_unit='kWh');db.add(row);db.flush()
 for f in model['factors']:db.add(ModelFactor(id=str(uuid4()),model_id=row.id,**f))
 for f in model['interactions']:db.add(ModelInteraction(id=str(uuid4()),model_id=row.id,**f))
 db.commit();return row
