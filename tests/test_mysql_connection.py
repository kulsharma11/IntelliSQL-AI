from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:mysql@127.0.0.1:3306/analytics_db"
)

with engine.connect() as conn:
    print("✅ Connected Successfully")