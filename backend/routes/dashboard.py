from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import DashboardResponse
from crud import get_dashboard_summary

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db)):
    """
    获取医院管理系统仪表盘统计数据

    返回包含以下信息的统计数据：
    - 基本统计：总患者数、总医生数、今日预约数、本周预约数、待处理病例数
    - 近期预约：最近5个预约记录
    - 部门统计：各科室的医生数量和预约数量综合统计
    """
    dashboard_data = get_dashboard_summary(db)
    return dashboard_data
