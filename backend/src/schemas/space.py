from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,FiniteFloat,model_validator
class SpaceCreate(BaseModel):
 model_config=ConfigDict(extra='forbid')
 name:str=Field(min_length=2,max_length=180)
 model_id:str
 description:str=Field(default='',max_length=3000)
 ranges_csv:str=Field(min_length=10,max_length=8000)
