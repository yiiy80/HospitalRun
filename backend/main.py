from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# 导入路由
from routes.patients import router as patients_router
from routes.doctors import router as doctors_router
from routes.appointments import router as appointments_router
from routes.dashboard import router as dashboard_router

# 创建数据库表
from database import Base, engine
from models import Patient, Doctor, Appointment

# 创建应用
app = FastAPI(
    title="HospitalRun API",
    description="医院管理系统后端API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "系统内部错误，请稍后重试",
                "details": str(exc) if app.debug else None
            }
        }
    )

# 包含路由
app.include_router(patients_router, prefix="/api")
app.include_router(doctors_router, prefix="/api")
app.include_router(appointments_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")

# 健康检查端点
@app.get("/health", tags=["health"])
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}

# 创建数据库表
@app.on_event("startup")
async def create_tables():
    """应用启动时创建数据库表"""
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")

# 根路径
@app.get("/", tags=["root"])
async def read_root():
    """
    HospitalRun API 根路径

    访问 /docs 查看API文档
    """
    return {
        "message": "HospitalRun API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
