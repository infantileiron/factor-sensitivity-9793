from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,FiniteFloat,model_validator
class ReportCreate(BaseModel):
 model_config=ConfigDict(extra='forbid')
 review_id:str
 title:str=Field(min_length=2,max_length=180)
