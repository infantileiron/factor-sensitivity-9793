from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,FiniteFloat,model_validator
class ReviewCreate(BaseModel):
 model_config=ConfigDict(extra='forbid')
 run_id:str
 action:str=Field(min_length=8,max_length=4000)
