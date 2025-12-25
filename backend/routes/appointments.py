from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from schemas import *
import crud

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=SuccessResponse)
async def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    """
    创建新预约

    - **patient_name**: 患者姓名 (必填)
    - **doctor_name**: 医生姓名 (必填)
    - **appointment_time**: 预约时间 (必填, 必须是未来时间)
    - **status**: 预约状态 (默认为"pending")
    - **reason**: 预约原因 (可选)
    - **notes**: 备注信息 (可选)
    """
    try:
        db_appointment = crud.create_appointment(db, appointment)
        response = SuccessResponse(
            success=True,
            data=Appointment.from_orm(db_appointment),
            message="预约创建成功"
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{appointment_id}", response_model=SuccessResponse)
async def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取预约信息
    """
    db_appointment = crud.get_appointment(db, appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="预约不存在")
    return SuccessResponse(success=True, data=Appointment.from_orm(db_appointment))

@router.get("/", response_model=AppointmentListResponse)
async def read_appointments(
    date_from: Optional[str] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="结束日期 (YYYY-MM-DD)"),
    status: Optional[str] = Query(None, description="预约状态"),
    doctor: Optional[str] = Query(None, description="医生姓名"),
    patient: Optional[str] = Query(None, description="患者姓名"),
    db: Session = Depends(get_db)
):
    """
    获取预约列表，支持日期范围、状态、医生和患者筛选
    返回数据包含患者和医生详细信息
    """
    appointments, today_summary = crud.get_appointments(
        db=db,
        date_from=date_from,
        date_to=date_to,
        status=status,
        doctor=doctor,
        patient=patient
    )

    return AppointmentListResponse(
        appointments=appointments,
        today_summary=today_summary
    )

@router.put("/{appointment_id}", response_model=SuccessResponse)
async def update_appointment(
    appointment_id: int,
    appointment: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    """
    更新预约信息

    注意：编辑预约时预约时间可以是过去的日期
    """
    db_appointment = crud.update_appointment(db, appointment_id, appointment)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="预约不存在")
    return SuccessResponse(
        success=True,
        data=Appointment.from_orm(db_appointment),
        message="预约更新成功"
    )

@router.delete("/{appointment_id}", response_model=SuccessResponse)
async def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    """
    删除预约
    """
    success = crud.delete_appointment(db, appointment_id)
    if not success:
        raise HTTPException(status_code=404, detail="预约不存在")
    return SuccessResponse(success=True, message="预约删除成功")
