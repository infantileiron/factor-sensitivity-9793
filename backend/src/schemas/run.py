from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,FiniteFloat,model_validator
class RunCreate(BaseModel):
 model_config=ConfigDict(extra='forbid')
 study_id:str
