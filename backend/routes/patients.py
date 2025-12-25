from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from schemas import *
import crud

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=SuccessResponse)
async def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    """
    创建新患者

    - **name**: 患者姓名 (必填)
    - **age**: 年龄 (必填, 0-150岁)
    - **gender**: 性别 (男/女)
    - **phone**: 联系电话 (可选)
    - **address**: 家庭地址 (可选)
    - **medical_condition**: 病情描述 (必填)
    - **notes**: 备注信息 (可选)
    """
    try:
        db_patient = crud.create_patient(db, patient)
        response = SuccessResponse(
            success=True,
            data=Patient.from_orm(db_patient),
            message="患者创建成功"
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{patient_id}", response_model=SuccessResponse)
async def read_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取患者信息
    """
    db_patient = crud.get_patient(db, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="患者不存在")
    return SuccessResponse(success=True, data=Patient.from_orm(db_patient))

@router.get("/", response_model=PatientListResponse)
async def read_patients(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(10, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索姓名/电话/病情"),
    gender: Optional[str] = Query(None, description="性别筛选 (男/女)"),
    db: Session = Depends(get_db)
):
    """
    获取患者列表，支持分页、搜索和筛选
    """
    skip = (page - 1) * limit
    patients, total = crud.get_patients(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        gender=gender
    )

    total_pages = (total + limit - 1) // limit  # 向上取整

    # 将SQLAlchemy对象转换为Pydantic对象
    patient_models = [Patient.from_orm(patient) for patient in patients]

    return PatientListResponse(
        patients=patient_models,
        pagination={
            "page": page,
            "limit": limit,
            "total": total,
            "totalPages": total_pages
        }
    )

@router.put("/{patient_id}", response_model=SuccessResponse)
async def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db)
):
    """
    更新患者信息
    """
    db_patient = crud.update_patient(db, patient_id, patient)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="患者不存在")
    return SuccessResponse(
        success=True,
        data=Patient.from_orm(db_patient),
        message="患者信息更新成功"
    )

@router.delete("/{patient_id}", response_model=SuccessResponse)
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    删除患者
    """
    success = crud.delete_patient(db, patient_id)
    if not success:
        raise HTTPException(status_code=404, detail="患者不存在")
    return SuccessResponse(success=True, message="患者删除成功")
