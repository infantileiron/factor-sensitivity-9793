from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.study import SensitivityStudy
from ..models.response_model import ResponseModel
from ..models.space import FactorSpace
def create(db,body):
 model=db.get(ResponseModel,body.model_id);space=db.get(FactorSpace,body.space_id)
 if not model or not space or space.model_id!=model.id:raise HTTPException(422,'模型与因子范围须存在且对应')
 if db.scalar(select(SensitivityStudy).where(SensitivityStudy.name==body.name)):raise HTTPException(409,'研究名称已存在')
 row=SensitivityStudy(id=str(uuid4()),**body.model_dump());db.add(row);db.commit();return row
