"""Morris elementary effects in normalized factor coordinates."""
import numpy as np
from .polynomial import validate_model,validate_ranges,physical_points,evaluate,integer

def morris(model,ranges,trajectories=24,levels=6,seed=20261112):
 model=validate_model(model);ranges=validate_ranges(model,ranges);d=len(ranges)
 trajectories=integer(trajectories,'轨迹数',2,128);levels=integer(levels,'网格级数',2,20);seed=integer(seed,'seed',0,2**32-1)
 if levels%2:raise ValueError('Morris网格级数p必须为偶数')
 rng=np.random.default_rng(seed);jump=levels//2;delta=jump/(levels-1);effects=[[] for _ in range(d)];paths=[]
 for trajectory in range(trajectories):
  direction=rng.choice([-1,1],size=d);indices=np.array([rng.integers(0,levels-jump) if sign>0 else rng.integers(jump,levels) for sign in direction]);order=rng.permutation(d);units=[indices.copy()/(levels-1)]
  for factor in order:
   indices=indices.copy();indices[factor]+=int(direction[factor])*jump;units.append(indices/(levels-1))
  unit=np.asarray(units,dtype=np.float64);physical=physical_points(unit,ranges);responses=evaluate(model,physical);steps=[]
  for step,factor in enumerate(order):
   signed_step=float(unit[step+1,factor]-unit[step,factor]);effect=float((responses[step+1]-responses[step])/signed_step);effects[factor].append(effect)
   steps.append({'factor_id':model['factors'][factor]['factor_id'],'signed_step':signed_step,'effect':effect})
  paths.append({'trajectory':trajectory+1,'normalized':unit.tolist(),'physical':physical.tolist(),'responses':responses.tolist(),'steps':steps})
 rows=[]
 for i,values in enumerate(effects):
  a=np.asarray(values,dtype=np.float64);rows.append({'factor_id':model['factors'][i]['factor_id'],'mu':float(a.mean()),'mu_star':float(np.abs(a).mean()),'sigma':float(a.std(ddof=1)),'effects':values,'effect_count':trajectories,'sigma_denominator':trajectories-1})
 return {'indices':rows,'trajectories':paths,'trajectory_count':trajectories,'levels':levels,'delta':delta,'seed':seed,'evaluations':trajectories*(d+1),'method':'Morris grid signed-step elementary effects','effect_unit':'kWh per normalized factor unit','sigma_ddof':1,'note':'EE除以归一空间实际有符号步长；sigma为跨轨迹样本标准差，不是均值标准误或置信区间。'}
