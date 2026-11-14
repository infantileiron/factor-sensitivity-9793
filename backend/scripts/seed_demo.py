import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from sqlalchemy import select,func
from src.config.database import Session,initialize
from src.models.user import User
from src.models.response_model import ResponseModel
from src.models.model_factor import ModelFactor
from src.models.model_interaction import ModelInteraction
from src.models.space import FactorSpace
from src.models.factor_range import FactorRange
from src.models.study import SensitivityStudy
from src.models.run import SensitivityRun
from src.models.review import FactorReview
from src.models.report import Report
from src.utils.security import hash_password
from src.services.run_service import compute
def seed():
 initialize()
 with Session() as db:
  for role in ['admin','analyst','viewer']:
   if not db.get(User,'seed-'+role):db.add(User(id='seed-'+role,email=role+'@sensitivity.demo',password_hash=hash_password('FactorDemo2026!'),role=role))
  models=[('demo-model','XH-C06 冷却电耗模拟代理',240,[('flow','冷却水流量','m³/h',3.5,.08,18,30),('inlet','入口水温','°C',14,.12,25,33),('load','热负荷比','1',650,85,.45,.95),('fan','风机频率','Hz',2.2,.025,30,50),('approach','逼近温差','°C',22,.7,3,8),('eff','泵效率','%',-4,.012,65,85)],[('load','fan',3.2),('inlet','approach',.75),('flow','load',1.8)]),('linear-model','手算线性 x + 2y',0,[('x','因子x','1',1,0,0,1),('y','因子y','1',2,0,0,1)],[]),('interaction-model','手算交互 x × y',0,[('x','因子x','1',0,0,0,1),('y','因子y','1',0,0,0,1)],[('x','y',1)])]
  for ident,name,intercept,factors,pairs in models:
   if not db.get(ResponseModel,ident):
    db.add(ResponseModel(id=ident,name=name,description='星衡能源节能研究组13人；XH-C06_202611.json受控模拟模型，独立均匀因子，不用于工业控制。',intercept=intercept,response_unit='kWh'));db.flush()
    for i,(fid,label,unit,linear,quadratic,low,high) in enumerate(factors):db.add(ModelFactor(id=ident+'-factor-'+str(i),model_id=ident,factor_id=fid,name=label,unit=unit,linear=linear,quadratic=quadratic))
    for i,(left,right,coefficient) in enumerate(pairs):db.add(ModelInteraction(id=ident+'-pair-'+str(i),model_id=ident,left=left,right=right,coefficient=coefficient))
   spaceid='demo-space' if ident=='demo-model' else ident+'-space'
   if not db.get(FactorSpace,spaceid):
    db.add(FactorSpace(id=spaceid,name=name+' · 独立均匀范围',model_id=ident,description='范围内独立均匀采样；物理单位与代理模型相同。'));db.flush()
    for i,(fid,label,unit,linear,quadratic,low,high) in enumerate(factors):db.add(FactorRange(id=spaceid+'-'+str(i),space_id=spaceid,factor_id=fid,low=low,high=high))
  db.flush()
  if not db.get(SensitivityStudy,'demo-study'):db.add(SensitivityStudy(id='demo-study',name='XH-C06 归一因子敏感度底稿',model_id='demo-model',space_id='demo-space',trajectories=24,levels=6,power=12,seed=20261112))
  db.flush()
  if not db.get(SensitivityRun,'demo-run'):db.add(SensitivityRun(id='demo-run',study_id='demo-study',status='queued',result={},error=''))
  db.commit();run=db.get(SensitivityRun,'demo-run')
  if run.status=='queued':compute(db,'demo-run')
  run=db.get(SensitivityRun,'demo-run')
  if run.status=='completed':
   if not db.get(FactorReview,'demo-review'):db.add(FactorReview(id='demo-review',run_id='demo-run',action='已核对物理范围、归一EE分母与有限采样；仅模拟代理敏感度，不宣称真实节能收益。',state='approved',reviewer='admin@sensitivity.demo'));db.flush()
   if not db.get(Report,'demo-report'):db.add(Report(id='demo-report',review_id='demo-review',title='XH-C06 冷却代理因子底稿',snapshot={'result':run.result,'action':'已核对模拟代理假设与有限样本边界','reviewer':'admin@sensitivity.demo'}))
  db.commit();counts={t.__tablename__:db.scalar(select(func.count()).select_from(t)) for t in [User,ResponseModel,ModelFactor,ModelInteraction,FactorSpace,FactorRange,SensitivityStudy,SensitivityRun,FactorReview,Report]};print(json.dumps(counts));return counts
if __name__=='__main__':seed()
