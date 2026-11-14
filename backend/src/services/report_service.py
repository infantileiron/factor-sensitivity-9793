import csv,io
from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.review import FactorReview
from ..models.run import SensitivityRun
from ..models.report import Report
def create(db,body):
 review=db.get(FactorReview,body.review_id)
 if not review or review.state!='approved':raise HTTPException(409,'须先批准因子复核')
 existing=db.scalar(select(Report).where(Report.review_id==review.id))
 if existing:return existing
 run=db.get(SensitivityRun,review.run_id);row=Report(id=str(uuid4()),review_id=review.id,title=body.title,snapshot={'result':run.result,'action':review.action,'reviewer':review.reviewer});db.add(row);db.commit();return row
def export(row):
 r=row.snapshot['result'];out=io.StringIO();writer=csv.writer(out);writer.writerow(['factor_id','name','physical_unit','low','high','mu_kwh_per_normalized_unit','mu_star','sigma_ddof1','morris_r','sigma_denominator','sobol_s1','jansen_st','st_minus_s1','base_n','morris_evaluations','sobol_evaluations','response_variance_ddof0','levels','delta','seed','assumptions','input_sha256'])
 for f in r['metrics']:writer.writerow([f['factor_id'],f['name'],f['unit'],f['low'],f['high'],f['mu'],f['mu_star'],f['sigma'],f['effect_count'],f['sigma_denominator'],f['s1'],f['st'],f['gap'],r['sobol']['base_samples'],r['morris']['evaluations'],r['sobol']['evaluations'],r['sobol']['response_variance'],r['morris']['levels'],r['morris']['delta'],r['config']['seed'],r['assumptions'],r['input_sha256']])
 return '\ufeff'+out.getvalue()
