"""Scrambled 2d Sobol A/B, centered Saltelli S1 and Jansen ST."""
import numpy as np
from scipy.stats import qmc
from .polynomial import validate_model,validate_ranges,physical_points,evaluate,integer

def sobol(model,ranges,power=12,seed=20261112):
 model=validate_model(model);ranges=validate_ranges(model,ranges);d=len(ranges);power=integer(power,'Sobol指数m',2,16);seed=integer(seed,'seed',0,2**32-1)
 unit=qmc.Sobol(d=2*d,scramble=True,seed=seed).random_base2(power);a,b=unit[:,:d],unit[:,d:];ya,yb=evaluate(model,physical_points(a,ranges)),evaluate(model,physical_points(b,ranges));combined=np.concatenate((ya,yb));mean=float(combined.mean());variance=float(np.mean((combined-mean)**2))
 if not np.isfinite(variance) or variance<=0:raise ValueError('代理响应方差为0或非有限，Sobol指数不可估')
 rows=[];warnings=[]
 for i,factor in enumerate(model['factors']):
  ab=a.copy();ab[:,i]=b[:,i];yab=evaluate(model,physical_points(ab,ranges));s1=float(np.mean((yb-mean)*(yab-ya))/variance);st=float(np.mean((ya-yab)**2)/(2*variance))
  if not np.isfinite([s1,st]).all():raise ValueError('Sobol指数非有限')
  rows.append({'factor_id':factor['factor_id'],'s1':s1,'st':st,'gap':st-s1})
  if s1<0 or s1>1 or st<0 or st>1:warnings.append(factor['factor_id']+'有限样本指数超出[0,1]，保留原值，不硬裁剪')
 if power<10:warnings.append('当前基础样本量较小，有限样本误差可能明显；点估计不作为置信区间')
 return {'indices':rows,'base_samples':2**power,'power':power,'dimension':2*d,'seed':seed,'evaluations':(d+2)*2**power,'response_mean':mean,'response_variance':variance,'variance_ddof':0,'method':'scrambled Sobol(2d); centered Saltelli S1 / Jansen ST','warnings':warnings,'note':'独立均匀因子范围；VarY为A/B合并总体方差。有限样本点估计，无置信区间或真实节能收益承诺。'}
