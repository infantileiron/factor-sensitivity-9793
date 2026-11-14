from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,FiniteFloat,model_validator
class ModelCreate(BaseModel):
 model_config=ConfigDict(extra='forbid')
 name:str=Field(min_length=2,max_length=180)
 description:str=Field(default='',max_length=3000)
 intercept:FiniteFloat=0
 response_unit:Literal['kWh']='kWh'
 factors_csv:str=Field(min_length=10,max_length=12000)
 interactions_csv:str=Field(default='left,right,coefficient',max_length=5000)
class ModelPatch(BaseModel):
 model_config=ConfigDict(extra='forbid')
 description:str=Field(max_length=3000)
