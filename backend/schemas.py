from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# 性别枚举
class GenderEnum(str, Enum):
    male = "男"
    female = "女"

# 医生专业枚举
class SpecialtyEnum(str, Enum):
    internal_medicine = "内科"
    surgery = "外科"
    pediatrics = "儿科"
    gynecology = "妇产科"
    ophthalmology = "眼科"
    dentistry = "口腔科"

# 医生状态枚举
class DoctorStatusEnum(str, Enum):
    on_duty = "在职"
    on_leave = "休息中"
    resigned = "离职"

# 预约状态枚举
class AppointmentStatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

# ============================================
# 患者相关Schemas
# ============================================

class PatientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="患者姓名")
    age: int = Field(..., ge=0, le=150, description="年龄")
    gender: GenderEnum = Field(..., description="性别")
    phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    address: Optional[str] = Field(None, max_length=500, description="家庭地址")
    medical_condition: str = Field(..., description="病情描述")
    notes: Optional[str] = Field(None, description="备注信息")

class PatientCreate(PatientBase):
    pass

class PatientUpdate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PatientListResponse(BaseModel):
    patients: List[Patient]
    pagination: Dict[str, Any]

# ============================================
# 医生相关Schemas
# ============================================

class DoctorBase(BaseModel):
    name: str = Field(..., max_length=100, description="医生姓名")
    specialty: SpecialtyEnum = Field(..., description="专业科室")
    experience: str = Field(..., max_length=50, description="工作经验")
    phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    status: DoctorStatusEnum = Field(DoctorStatusEnum.on_duty, description="工作状态")
    notes: Optional[str] = Field(None, description="备注信息")

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DoctorListResponse(BaseModel):
    doctors: List[Doctor]
    summary: Dict[str, Any]

# ============================================
# 预约相关Schemas
# ============================================

class AppointmentBase(BaseModel):
    patient_name: str = Field(..., max_length=100, description="患者姓名")
    doctor_name: str = Field(..., max_length=100, description="医生姓名")
    appointment_time: datetime = Field(..., description="预约时间")
    status: AppointmentStatusEnum = Field(AppointmentStatusEnum.pending, description="预约状态")
    reason: Optional[str] = Field(None, description="预约原因")
    notes: Optional[str] = Field(None, description="备注信息")

class AppointmentCreate(AppointmentBase):
    @validator('appointment_time')
    def validate_appointment_time_future(cls, v):
        if v < datetime.now():
            raise ValueError('预约时间必须是未来的时间')
        return v

class AppointmentUpdate(AppointmentBase):
    @validator('appointment_time')
    def validate_appointment_time_future_edit(cls, v):
        # 编辑时不强制验证未来时间
        return v

class Appointment(AppointmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AppointmentWithDetails(Appointment):
    patient: Optional[Dict[str, Any]] = None
    doctor: Optional[Dict[str, Any]] = None

class AppointmentListResponse(BaseModel):
    appointments: List[AppointmentWithDetails]
    today_summary: Dict[str, Any]

# ============================================
# 通用Schemas
# ============================================

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None

class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail

# ============================================
# Dashboard Schemas
# ============================================

class DashboardSummary(BaseModel):
    total_patients: int
    total_doctors: int
    total_appointments_today: int
    appointments_this_week: int
    pending_cases: int

class RecentAppointment(BaseModel):
    id: int
    patient_name: str
    doctor_name: str
    appointment_time: datetime
    status: AppointmentStatusEnum
    reason: Optional[str]

class DepartmentSummary(BaseModel):
    name: str
    doctor_count: int
    appointment_count: int

class DashboardResponse(BaseModel):
    summary: DashboardSummary
    recent_appointments: List[RecentAppointment]
    departments: List[DepartmentSummary]
