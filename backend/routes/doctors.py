from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from schemas import *
import crud

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=SuccessResponse)
async def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db)
):
    """
    创建新医生

    - **name**: 医生姓名 (必填)
    - **specialty**: 专业科室 (必填)
    - **experience**: 工作经验 (必填)
    - **phone**: 联系电话 (可选)
    - **status**: 工作状态 (默认为"在职")
    - **notes**: 备注信息 (可选)
    """
    try:
        db_doctor = crud.create_doctor(db, doctor)
        response = SuccessResponse(
            success=True,
            data=Doctor.from_orm(db_doctor),
            message="医生创建成功"
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{doctor_id}", response_model=SuccessResponse)
async def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取医生信息
    """
    db_doctor = crud.get_doctor(db, doctor_id)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="医生不存在")
    return SuccessResponse(success=True, data=Doctor.from_orm(db_doctor))

@router.get("/", response_model=DoctorListResponse)
async def read_doctors(
    specialty: Optional[str] = Query(None, description="专业科室筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    search: Optional[str] = Query(None, description="搜索医生姓名"),
    db: Session = Depends(get_db)
):
    """
    获取医生列表，支持专业、状态和姓名的筛选
    """
    doctors, summary = crud.get_doctors(
        db=db,
        specialty=specialty,
        status=status,
        search=search
    )

    # 将SQLAlchemy对象转换为Pydantic对象
    doctor_models = [Doctor.from_orm(doctor) for doctor in doctors]

    return DoctorListResponse(
        doctors=doctor_models,
        summary=summary
    )

@router.put("/{doctor_id}", response_model=SuccessResponse)
async def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db)
):
    """
    更新医生信息
    """
    db_doctor = crud.update_doctor(db, doctor_id, doctor)
    if db_doctor is None:
        raise HTTPException(status_code=404, detail="医生不存在")
    return SuccessResponse(
        success=True,
        data=Doctor.from_orm(db_doctor),
        message="医生信息更新成功"
    )

@router.delete("/{doctor_id}", response_model=SuccessResponse)
async def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    删除医生
    """
    success = crud.delete_doctor(db, doctor_id)
    if not success:
        raise HTTPException(status_code=404, detail="医生不存在")
    return SuccessResponse(success=True, message="医生删除成功")
