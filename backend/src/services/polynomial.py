"""Controlled polynomial response; coefficients are data, never executable expressions."""
import math,re
import numpy as np

def finite(value,label):
 if isinstance(value,bool):raise ValueError(label+'必须为有限数')
 try:value=float(value)
 except (ValueError,TypeError):raise ValueError(label+'必须为有限数')
 if not math.isfinite(value):raise ValueError(label+'必须为有限数')
 return value

def validate_model(model):
 factors=model.get('factors',[])
 if not 2<=len(factors)<=6:raise ValueError('模型必须含2–6个因子')
 ids=[];clean=[]
 for factor in factors:
  ident=str(factor.get('factor_id',''))
  if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,31}',ident) or ident in ids:raise ValueError('因子ID非法或重复')
  ids.append(ident);linear=finite(factor.get('linear',0),'线性系数');quadratic=finite(factor.get('quadratic',0),'二次系数')
  if max(abs(linear),abs(quadratic))>1e6:raise ValueError('系数绝对值不能超过1e6')
  clean.append({'factor_id':ident,'name':str(factor.get('name') or ident),'unit':str(factor.get('unit') or '1'),'linear':linear,'quadratic':quadratic})
 interactions=[];seen=set()
 for pair in model.get('interactions',[]):
  left,right=str(pair.get('left','')),str(pair.get('right',''))
  if left not in ids or right not in ids or left==right:raise ValueError('交互项因子未知或自身交互')
  key=tuple(sorted((left,right)))
  if key in seen:raise ValueError('重复交互项（含反向重复）')
  seen.add(key);coefficient=finite(pair.get('coefficient'),'交互系数')
  if abs(coefficient)>1e6:raise ValueError('交互系数绝对值不能超过1e6')
  interactions.append({'left':left,'right':right,'coefficient':coefficient})
 intercept=finite(model.get('intercept',0),'截距')
 if abs(intercept)>1e12:raise ValueError('截距绝对值不能超过1e12')
 return {'intercept':intercept,'factors':clean,'interactions':interactions,'response_unit':'kWh'}

def validate_ranges(model,ranges):
 model=validate_model(model);ids=[f['factor_id'] for f in model['factors']];rows={}
 for row in ranges:
  ident=row.get('factor_id')
  if ident not in ids or ident in rows:raise ValueError('范围因子未知或重复')
  low,high=finite(row.get('low'),'范围下界'),finite(row.get('high'),'范围上界')
  if not low<high or max(abs(low),abs(high))>1e4:raise ValueError('因子范围须正宽，端点绝对值不超过10000')
  rows[ident]={'factor_id':ident,'low':low,'high':high}
 if set(rows)!=set(ids):raise ValueError('因子范围须完整覆盖模型')
 return [rows[ident] for ident in ids]

def evaluate(model,physical):
 model=validate_model(model);x=np.asarray(physical,dtype=np.float64);d=len(model['factors'])
 if x.ndim!=2 or x.shape[1]!=d or not np.isfinite(x).all():raise ValueError('模型输入维度或有限性不合法')
 y=np.full(x.shape[0],model['intercept'],dtype=np.float64);index={f['factor_id']:i for i,f in enumerate(model['factors'])}
 with np.errstate(over='ignore',invalid='ignore'):
  for i,f in enumerate(model['factors']):y+=f['linear']*x[:,i]+f['quadratic']*x[:,i]**2
  for pair in model['interactions']:y+=pair['coefficient']*x[:,index[pair['left']]]*x[:,index[pair['right']]]
 if not np.isfinite(y).all():raise ValueError('代理模型响应非有限')
 return y

def physical_points(unit,ranges):
 low=np.array([r['low'] for r in ranges],dtype=np.float64);width=np.array([r['high']-r['low'] for r in ranges],dtype=np.float64)
 return low+np.asarray(unit,dtype=np.float64)*width

def integer(value,label,low,high):
 if isinstance(value,bool) or not isinstance(value,(int,np.integer)) or not low<=value<=high:raise ValueError(f'{label}须为{low}–{high}的整数')
 return int(value)
