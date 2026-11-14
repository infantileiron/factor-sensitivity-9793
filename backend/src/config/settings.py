import os
DATABASE_URL=os.getenv("DATABASE_URL","mysql+pymysql://sensitivity:sensitivity_demo@localhost:17733/sensitivity")
REDIS_URL=os.getenv("REDIS_URL","redis://localhost:6379/0")
JWT_SECRET=os.getenv("JWT_SECRET","factor-sensitivity-local-demo-change-before-deployment")
SEED_DEMO=os.getenv("SEED_DEMO","true").lower()=="true"
