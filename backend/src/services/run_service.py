import json,hashlib
from uuid import uuid4
from fastapi import HTTPException
from ..models.run import SensitivityRun
from ..models.study import SensitivityStudy
from ..models.response_model import ResponseModel
from ..models.space import FactorSpace
from ..models.factor_metric import FactorMetric
from ..models.elementary_effect import ElementaryEffect
from ..models.evaluation import EvaluationPoint
from ..utils.queue import enqueue
from .model_service import specification
from .space_service import ranges
from .polynomial import validate_ranges
from .morris import morris
from .sobol import sobol
def create(db,body):
 if not db.get(SensitivityStudy,body.study_id):raise HTTPException(422,'敏感度研究不存在')
 row=SensitivityRun(id=str(uuid4()),study_id=body.study_id,status='queued',result={},error='');db.add(row);db.commit()
 try:enqueue(row.id)
 except Exception:
  row.status='failed';row.error='Redis队列不可用，请重试';db.commit();raise HTTPException(503,row.error)
 return row
def compute(db,ident):
 row=db.get(SensitivityRun,ident)
 if not row or row.status not in ['queued','running']:return
 row.status='running';db.commit()
 try:
  study=db.get(SensitivityStudy,row.study_id);modelrow=db.get(ResponseModel,study.model_id);spacerow=db.get(FactorSpace,study.space_id);model=specification(db,modelrow);bounds=validate_ranges(model,ranges(db,spacerow));config={k:getattr(study,k) for k in ['trajectories','levels','power','seed']}
  local=morris(model,bounds,study.trajectories,study.levels,study.seed);global_=sobol(model,bounds,study.power,study.seed)
  metrics=[{**f,**bounds[i],**local['indices'][i],**global_['indices'][i]} for i,f in enumerate(model['factors'])]
  fingerprint=hashlib.sha256(json.dumps({'model':model,'ranges':bounds,'config':config},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  row.result={'model_name':modelrow.name,'space_name':spacerow.name,'study_name':study.name,'model':model,'ranges':bounds,'config':config,'morris':local,'sobol':global_,'metrics':metrics,'warnings':global_['warnings'],'input_sha256':fingerprint,'assumptions':'受控多项式模拟代理；因子独立均匀分布。EE按归一空间步长；指数为有限样本点估计，无CI，不代表真实节能收益。'}
  row.response_mean=global_['response_mean'];row.response_variance=global_['response_variance']
  for metric in metrics:db.add(FactorMetric(id=str(uuid4()),run_id=row.id,**{k:metric[k] for k in ['factor_id','mu','mu_star','sigma','s1','st','gap','effect_count','sigma_denominator']}))
  for trajectory in local['trajectories']:
   for step,effect in enumerate(trajectory['steps']):db.add(ElementaryEffect(id=str(uuid4()),run_id=row.id,trajectory=trajectory['trajectory'],**effect))
   for step,response in enumerate(trajectory['responses']):db.add(EvaluationPoint(id=str(uuid4()),run_id=row.id,trajectory=trajectory['trajectory'],step=step,normalized=trajectory['normalized'][step],physical=trajectory['physical'][step],response=response))
  row.status='completed';db.commit()
 except Exception as error:
  db.rollback();row=db.get(SensitivityRun,ident);row.status='failed';row.error=str(error)[:1000];db.commit()
