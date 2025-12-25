"""
测试配置文件
提供测试所需的 fixtures 和配置
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

import sys
import os

# 添加父目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Base, get_db
from main import app
from models import Patient, Doctor, Appointment


# 测试数据库配置 - 使用内存 SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_engine():
    """创建测试数据库引擎"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(test_engine):
    """创建测试数据库会话"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(test_db):
    """创建测试客户端"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


# ============================================
# 测试数据 Fixtures
# ============================================

@pytest.fixture
def sample_patient_data():
    """示例患者数据"""
    return {
        "name": "张三",
        "age": 35,
        "gender": "男",
        "phone": "13800138000",
        "address": "北京市朝阳区",
        "medical_condition": "感冒发烧",
        "notes": "需要复查"
    }


@pytest.fixture
def sample_doctor_data():
    """示例医生数据"""
    return {
        "name": "李医生",
        "specialty": "内科",
        "experience": "10年",
        "phone": "13900139000",
        "status": "在职",
        "notes": "主任医师"
    }


@pytest.fixture
def sample_appointment_data():
    """示例预约数据"""
    future_time = datetime.now() + timedelta(days=1)
    return {
        "patient_name": "张三",
        "doctor_name": "李医生",
        "appointment_time": future_time.isoformat(),
        "status": "pending",
        "reason": "定期复查",
        "notes": "请空腹"
    }


@pytest.fixture
def create_patient(test_db):
    """创建测试患者的工厂函数"""
    def _create_patient(**kwargs):
        defaults = {
            "name": "测试患者",
            "age": 30,
            "gender": "男",
            "medical_condition": "测试病情"
        }
        defaults.update(kwargs)
        patient = Patient(**defaults)
        test_db.add(patient)
        test_db.commit()
        test_db.refresh(patient)
        return patient
    return _create_patient


@pytest.fixture
def create_doctor(test_db):
    """创建测试医生的工厂函数"""
    def _create_doctor(**kwargs):
        defaults = {
            "name": "测试医生",
            "specialty": "内科",
            "experience": "5年",
            "status": "在职"
        }
        defaults.update(kwargs)
        doctor = Doctor(**defaults)
        test_db.add(doctor)
        test_db.commit()
        test_db.refresh(doctor)
        return doctor
    return _create_doctor


@pytest.fixture
def create_appointment(test_db):
    """创建测试预约的工厂函数"""
    def _create_appointment(**kwargs):
        defaults = {
            "patient_name": "测试患者",
            "doctor_name": "测试医生",
            "appointment_time": datetime.now() + timedelta(days=1),
            "status": "pending"
        }
        defaults.update(kwargs)
        appointment = Appointment(**defaults)
        test_db.add(appointment)
        test_db.commit()
        test_db.refresh(appointment)
        return appointment
    return _create_appointment


# ============================================
# 批量测试数据 Fixtures
# ============================================

@pytest.fixture
def multiple_patients(test_db):
    """创建多个测试患者"""
    patients = []
    for i in range(5):
        patient = Patient(
            name=f"患者{i+1}",
            age=20 + i * 10,
            gender="男" if i % 2 == 0 else "女",
            phone=f"1380013800{i}",
            medical_condition=f"病情{i+1}"
        )
        test_db.add(patient)
        patients.append(patient)
    test_db.commit()
    return patients


@pytest.fixture
def multiple_doctors(test_db):
    """创建多个测试医生"""
    doctors = []
    specialties = ["内科", "外科", "儿科", "妇产科", "眼科", "口腔科"]
    for i, specialty in enumerate(specialties):
        doctor = Doctor(
            name=f"{specialty}医生",
            specialty=specialty,
            experience=f"{(i+1)*5}年",
            status="在职"
        )
        test_db.add(doctor)
        doctors.append(doctor)
    test_db.commit()
    return doctors


@pytest.fixture
def multiple_appointments(test_db, multiple_patients, multiple_doctors):
    """创建多个测试预约"""
    appointments = []
    for i in range(3):
        appointment = Appointment(
            patient_name=multiple_patients[i].name,
            doctor_name=multiple_doctors[i].name,
            appointment_time=datetime.now() + timedelta(days=i+1),
            status="pending",
            reason=f"预约原因{i+1}"
        )
        test_db.add(appointment)
        appointments.append(appointment)
    test_db.commit()
    return appointments


# ============================================
# 工具函数
# ============================================

@pytest.fixture
def assert_response_success():
    """验证成功响应的辅助函数"""
    def _assert(response, status_code=200):
        assert response.status_code == status_code
        data = response.json()
        assert data.get("success") is True or "success" not in data
        return data
    return _assert


@pytest.fixture
def assert_response_error():
    """验证错误响应的辅助函数"""
    def _assert(response, status_code=400):
        assert response.status_code == status_code
        if status_code >= 400:
            data = response.json()
            # FastAPI 默认错误格式或自定义格式
            assert "detail" in data or "error" in data
        return response.json()
    return _assert
