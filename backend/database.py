from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

# 数据库URL - 从.env文件或环境变量读取
DATABASE_URL = os.getenv("DATABASE_URL", "")

# 创建SQLAlchemy引擎
engine = create_engine(DATABASE_URL, echo=True)

# 创建Session类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Base类
Base = declarative_base()

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
