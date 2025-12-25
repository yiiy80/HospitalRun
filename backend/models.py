from sqlalchemy import Column, Integer, String, Text, DateTime, func, Enum
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='患者ID')
    name = Column(String(100), nullable=False, comment='患者姓名')
    age = Column(Integer, nullable=False, comment='年龄')
    gender = Column(Enum('男', '女'), nullable=False, comment='性别')
    phone = Column(String(20), comment='联系电话')
    address = Column(Text, comment='家庭地址')
    medical_condition = Column(Text, nullable=False, comment='病情描述')
    notes = Column(Text, comment='备注信息')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='医生ID')
    name = Column(String(100), nullable=False, comment='医生姓名')
    specialty = Column(Enum('内科', '外科', '儿科', '妇产科', '眼科', '口腔科'), nullable=False, comment='专业科室')
    experience = Column(String(50), nullable=False, comment='工作经验（如：10年）')
    phone = Column(String(20), comment='联系电话')
    status = Column(Enum('在职', '休息中', '离职'), nullable=False, default='在职', comment='工作状态')
    notes = Column(Text, comment='备注信息（如：主任医师）')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='预约ID')
    patient_name = Column(String(100), nullable=False, comment='患者姓名')
    doctor_name = Column(String(100), nullable=False, comment='医生姓名')
    appointment_time = Column(DateTime, nullable=False, comment='预约时间')
    status = Column(Enum('pending', 'confirmed', 'cancelled'), nullable=False, default='pending', comment='预约状态：待确认/已确认/已取消')
    reason = Column(Text, comment='预约原因')
    notes = Column(Text, comment='备注信息')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')
