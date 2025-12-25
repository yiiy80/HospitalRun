from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from models import Patient, Doctor, Appointment
from schemas import (
    PatientCreate, PatientUpdate,
    DoctorCreate, DoctorUpdate,
    AppointmentCreate, AppointmentUpdate,
    GenderEnum, SpecialtyEnum
)
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

# ============================================
# 患者CRUD操作
# ============================================

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 10, search: str = None, gender: str = None):
    query = db.query(Patient)

    if search:
        query = query.filter(
            or_(
                Patient.name.contains(search),
                Patient.phone.contains(search),
                Patient.medical_condition.contains(search)
            )
        )

    if gender:
        if gender == "男":
            query = query.filter(Patient.gender == GenderEnum.male.value)
        elif gender == "女":
            query = query.filter(Patient.gender == GenderEnum.female.value)

    total = query.count()
    patients = query.offset(skip).limit(limit).all()

    return patients, total

def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def update_patient(db: Session, patient_id: int, patient: PatientUpdate):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        update_data = patient.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_patient, field, value)
        db.commit()
        db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = get_patient(db, patient_id)
    if db_patient:
        db.delete(db_patient)
        db.commit()
        return True
    return False

# ============================================
# 医生CRUD操作
# ============================================

def get_doctor(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()

def get_doctors(db: Session, specialty: str = None, status: str = None, search: str = None):
    query = db.query(Doctor)

    if specialty:
        # 转换前端传来的英文到中文
        specialty_map = {e.name: e.value for e in SpecialtyEnum}
        if specialty in specialty_map:
            query = query.filter(Doctor.specialty == specialty_map[specialty])

    if status:
        query = query.filter(Doctor.status == status)

    if search:
        query = query.filter(
            or_(
                Doctor.name.contains(search),
                Doctor.specialty.contains(search)
            )
        )

    doctors = query.all()

    # 统计信息
    total = len(doctors)
    specialty_count = {}
    status_count = {}

    for doctor in doctors:
        spec = doctor.specialty
        stat = doctor.status

        specialty_count[spec] = specialty_count.get(spec, 0) + 1
        status_count[stat] = status_count.get(stat, 0) + 1

    return doctors, {
        "total": total,
        "specialty_count": specialty_count,
        "status_count": status_count
    }

def create_doctor(db: Session, doctor: DoctorCreate):
    db_doctor = Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def update_doctor(db: Session, doctor_id: int, doctor: DoctorUpdate):
    db_doctor = get_doctor(db, doctor_id)
    if db_doctor:
        update_data = doctor.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_doctor, field, value)
        db.commit()
        db.refresh(db_doctor)
    return db_doctor

def delete_doctor(db: Session, doctor_id: int):
    db_doctor = get_doctor(db, doctor_id)
    if db_doctor:
        db.delete(db_doctor)
        db.commit()
        return True
    return False

# ============================================
# 预约CRUD操作
# ============================================

def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def get_appointments(
    db: Session,
    date_from: str = None,
    date_to: str = None,
    status: str = None,
    doctor: str = None,
    patient: str = None
):
    query = db.query(Appointment)

    if date_from:
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(Appointment.appointment_time >= date_from_obj)

    if date_to:
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
        date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
        query = query.filter(Appointment.appointment_time <= date_to_obj)

    if status:
        query = query.filter(Appointment.status == status)

    if doctor:
        query = query.filter(Appointment.doctor_name == doctor)

    if patient:
        query = query.filter(Appointment.patient_name == patient)

    appointments = query.all()

    # 增强数据：包含患者和医生详细信息
    enhanced_appointments = []
    for appointment in appointments:
        appointment_dict = {
            **appointment.__dict__,
            "patient": None,
            "doctor": None
        }

        # 获取患者信息
        patient_info = db.query(Patient).filter(
            Patient.name == appointment.patient_name
        ).first()
        if patient_info:
            appointment_dict["patient"] = {
                "name": patient_info.name,
                "age": patient_info.age,
                "gender": patient_info.gender,
                "phone": patient_info.phone,
                "condition": patient_info.medical_condition
            }

        # 获取医生信息
        doctor_info = db.query(Doctor).filter(
            Doctor.name == appointment.doctor_name
        ).first()
        if doctor_info:
            appointment_dict["doctor"] = {
                "name": doctor_info.name,
                "specialty": doctor_info.specialty,
                "experience": doctor_info.experience
            }

        enhanced_appointments.append(appointment_dict)

    # 今日统计
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())

    today_summary = {
        "total": db.query(Appointment).filter(
            and_(
                Appointment.appointment_time >= today_start,
                Appointment.appointment_time <= today_end
            )
        ).count(),
        "confirmed": db.query(Appointment).filter(
            and_(
                Appointment.appointment_time >= today_start,
                Appointment.appointment_time <= today_end,
                Appointment.status == 'confirmed'
            )
        ).count(),
        "pending": db.query(Appointment).filter(
            and_(
                Appointment.appointment_time >= today_start,
                Appointment.appointment_time <= today_end,
                Appointment.status == 'pending'
            )
        ).count(),
        "cancelled": db.query(Appointment).filter(
            and_(
                Appointment.appointment_time >= today_start,
                Appointment.appointment_time <= today_end,
                Appointment.status == 'cancelled'
            )
        ).count()
    }

    return enhanced_appointments, today_summary

def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def update_appointment(db: Session, appointment_id: int, appointment: AppointmentUpdate):
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        update_data = appointment.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_appointment, field, value)
        db.commit()
        db.refresh(db_appointment)
    return db_appointment

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = get_appointment(db, appointment_id)
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
        return True
    return False

# ============================================
# Dashboard统计操作
# ============================================

def get_dashboard_summary(db: Session):
    # 基本统计
    total_patients = db.query(Patient).count()
    total_doctors = db.query(Doctor).count()

    # 今日预约
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    total_appointments_today = db.query(Appointment).filter(
        and_(
            Appointment.appointment_time >= today_start,
            Appointment.appointment_time <= today_end
        )
    ).count()

    # 本周预约
    week_start = today - timedelta(days=today.weekday())
    week_start = datetime.combine(week_start, datetime.min.time())
    week_end = week_start + timedelta(days=6, hours=23, minutes=59, seconds=59)
    appointments_this_week = db.query(Appointment).filter(
        and_(
            Appointment.appointment_time >= week_start,
            Appointment.appointment_time <= week_end
        )
    ).count()

    # 待处理病例（假设有待确诊或待治疗状态的患者）
    pending_cases = db.query(Patient).filter(
        Patient.medical_condition.contains('复查') |
        Patient.medical_condition.contains('观察')
    ).count()

    # 近期预约
    recent_appointments = db.query(Appointment).filter(
        Appointment.appointment_time >= today_start
    ).order_by(Appointment.appointment_time).limit(5).all()

    # 科室统计
    departments = []
    specialties = db.query(Doctor.specialty, func.count(Doctor.id)).group_by(Doctor.specialty).all()

    for specialty, doctor_count in specialties:
        appointment_count = db.query(Appointment).filter(
            Appointment.doctor_name.in_(
                db.query(Doctor.name).filter(Doctor.specialty == specialty)
            )
        ).count()

        departments.append({
            "name": specialty,
            "doctor_count": doctor_count,
            "appointment_count": appointment_count
        })

    return {
        "summary": {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_appointments_today": total_appointments_today,
            "appointments_this_week": appointments_this_week,
            "pending_cases": pending_cases
        },
        "recent_appointments": recent_appointments,
        "departments": departments
    }
