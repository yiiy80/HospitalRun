"""
数据库模型测试
测试 SQLAlchemy 模型的创建、关系和约束
"""
import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models import Patient, Doctor, Appointment


class TestPatientModel:
    """患者模型测试"""

    def test_create_patient_with_required_fields(self, test_db):
        """测试创建患者 - 仅必填字段"""
        patient = Patient(
            name="张三",
            age=30,
            gender="男",
            medical_condition="感冒"
        )
        test_db.add(patient)
        test_db.commit()
        test_db.refresh(patient)

        assert patient.id is not None
        assert patient.name == "张三"
        assert patient.age == 30
        assert patient.gender == "男"
        assert patient.medical_condition == "感冒"
        assert patient.created_at is not None
        assert patient.updated_at is not None

    def test_create_patient_with_all_fields(self, test_db):
        """测试创建患者 - 所有字段"""
        patient = Patient(
            name="李四",
            age=25,
            gender="女",
            phone="13800138000",
            address="北京市朝阳区",
            medical_condition="体检",
            notes="无过敏史"
        )
        test_db.add(patient)
        test_db.commit()
        test_db.refresh(patient)

        assert patient.phone == "13800138000"
        assert patient.address == "北京市朝阳区"
        assert patient.notes == "无过敏史"

    def test_patient_missing_required_field(self, test_db):
        """测试缺少必填字段"""
        patient = Patient(
            name="王五",
            age=40
            # 缺少 gender 和 medical_condition
        )
        test_db.add(patient)

        with pytest.raises(IntegrityError):
            test_db.commit()
        test_db.rollback()

    @pytest.mark.skip(reason="SQLite does not enforce ENUM constraints - test only valid on MySQL")
    def test_patient_gender_constraint(self, test_db):
        """测试性别枚举约束"""
        patient = Patient(
            name="测试",
            age=30,
            gender="未知",  # 无效的性别值
            medical_condition="测试"
        )
        test_db.add(patient)

        with pytest.raises(Exception):  # MySQL会抛出枚举值错误
            test_db.commit()
        test_db.rollback()

    def test_patient_auto_timestamps(self, test_db):
        """测试自动时间戳"""
        patient = Patient(
            name="时间测试",
            age=30,
            gender="男",
            medical_condition="测试"
        )
        test_db.add(patient)
        test_db.commit()
        test_db.refresh(patient)

        created_at = patient.created_at
        updated_at = patient.updated_at

        assert created_at is not None
        assert updated_at is not None
        assert isinstance(created_at, datetime)
        assert isinstance(updated_at, datetime)

        # 更新记录
        patient.medical_condition = "已治愈"
        test_db.commit()
        test_db.refresh(patient)

        assert patient.created_at == created_at  # 创建时间不变
        # 注意: SQLite 的 onupdate 可能不触发，这是已知限制

    def test_patient_query_by_name(self, test_db, multiple_patients):
        """测试按姓名查询"""
        patient = test_db.query(Patient).filter(Patient.name == "患者1").first()
        assert patient is not None
        assert patient.name == "患者1"

    def test_patient_query_by_gender(self, test_db, multiple_patients):
        """测试按性别查询"""
        male_patients = test_db.query(Patient).filter(Patient.gender == "男").all()
        assert len(male_patients) == 3  # multiple_patients 创建了3个男性

    def test_patient_delete(self, test_db, create_patient):
        """测试删除患者"""
        patient = create_patient(name="待删除患者")
        patient_id = patient.id

        test_db.delete(patient)
        test_db.commit()

        deleted_patient = test_db.query(Patient).filter(Patient.id == patient_id).first()
        assert deleted_patient is None


class TestDoctorModel:
    """医生模型测试"""

    def test_create_doctor_with_required_fields(self, test_db):
        """测试创建医生 - 仅必填字段"""
        doctor = Doctor(
            name="王医生",
            specialty="内科",
            experience="5年"
        )
        test_db.add(doctor)
        test_db.commit()
        test_db.refresh(doctor)

        assert doctor.id is not None
        assert doctor.name == "王医生"
        assert doctor.specialty == "内科"
        assert doctor.experience == "5年"
        assert doctor.status == "在职"  # 默认值

    @pytest.mark.skip(reason="SQLite does not enforce ENUM constraints - test only valid on MySQL")
    def test_doctor_specialty_constraint(self, test_db):
        """测试专业科室枚举约束"""
        doctor = Doctor(
            name="测试医生",
            specialty="神经科",  # 不在枚举列表中
            experience="10年"
        )
        test_db.add(doctor)

        with pytest.raises(Exception):
            test_db.commit()
        test_db.rollback()

    def test_doctor_status_default_value(self, test_db):
        """测试状态默认值"""
        doctor = Doctor(
            name="新医生",
            specialty="外科",
            experience="3年"
        )
        test_db.add(doctor)
        test_db.commit()
        test_db.refresh(doctor)

        assert doctor.status == "在职"

    @pytest.mark.skip(reason="SQLite does not enforce ENUM constraints - test only valid on MySQL")
    def test_doctor_status_constraint(self, test_db):
        """测试状态枚举约束"""
        doctor = Doctor(
            name="测试医生",
            specialty="儿科",
            experience="5年",
            status="请假中"  # 无效的状态值
        )
        test_db.add(doctor)

        with pytest.raises(Exception):
            test_db.commit()
        test_db.rollback()

    def test_doctor_all_specialties(self, test_db):
        """测试所有有效的专业科室"""
        specialties = ["内科", "外科", "儿科", "妇产科", "眼科", "口腔科"]
        for specialty in specialties:
            doctor = Doctor(
                name=f"{specialty}医生",
                specialty=specialty,
                experience="5年"
            )
            test_db.add(doctor)

        test_db.commit()

        doctors = test_db.query(Doctor).all()
        assert len(doctors) == 6

    def test_doctor_query_by_specialty(self, test_db, multiple_doctors):
        """测试按专业查询"""
        internal_doctors = test_db.query(Doctor).filter(Doctor.specialty == "内科").all()
        assert len(internal_doctors) == 1
        assert internal_doctors[0].name == "内科医生"

    def test_doctor_update_status(self, test_db, create_doctor):
        """测试更新医生状态"""
        doctor = create_doctor(name="在职医生", status="在职")

        doctor.status = "休息中"
        test_db.commit()
        test_db.refresh(doctor)

        assert doctor.status == "休息中"


class TestAppointmentModel:
    """预约模型测试"""

    def test_create_appointment_with_required_fields(self, test_db):
        """测试创建预约 - 仅必填字段"""
        appointment = Appointment(
            patient_name="张三",
            doctor_name="李医生",
            appointment_time=datetime(2025, 12, 15, 10, 0, 0)
        )
        test_db.add(appointment)
        test_db.commit()
        test_db.refresh(appointment)

        assert appointment.id is not None
        assert appointment.patient_name == "张三"
        assert appointment.doctor_name == "李医生"
        assert appointment.status == "pending"  # 默认值

    def test_appointment_status_default_value(self, test_db):
        """测试预约状态默认值"""
        appointment = Appointment(
            patient_name="患者",
            doctor_name="医生",
            appointment_time=datetime(2025, 12, 20, 14, 0, 0)
        )
        test_db.add(appointment)
        test_db.commit()
        test_db.refresh(appointment)

        assert appointment.status == "pending"

    @pytest.mark.skip(reason="SQLite does not enforce ENUM constraints - test only valid on MySQL")
    def test_appointment_status_constraint(self, test_db):
        """测试状态枚举约束"""
        appointment = Appointment(
            patient_name="患者",
            doctor_name="医生",
            appointment_time=datetime(2025, 12, 20, 14, 0, 0),
            status="completed"  # 无效的状态值
        )
        test_db.add(appointment)

        with pytest.raises(Exception):
            test_db.commit()
        test_db.rollback()

    def test_appointment_all_statuses(self, test_db):
        """测试所有有效的预约状态"""
        statuses = ["pending", "confirmed", "cancelled"]
        for i, status in enumerate(statuses):
            appointment = Appointment(
                patient_name=f"患者{i}",
                doctor_name=f"医生{i}",
                appointment_time=datetime(2025, 12, 15 + i, 10, 0, 0),
                status=status
            )
            test_db.add(appointment)

        test_db.commit()

        appointments = test_db.query(Appointment).all()
        assert len(appointments) == 3

    def test_appointment_query_by_status(self, test_db, multiple_appointments):
        """测试按状态查询"""
        pending_appointments = test_db.query(Appointment).filter(
            Appointment.status == "pending"
        ).all()
        assert len(pending_appointments) == 3

    def test_appointment_query_by_doctor(self, test_db, multiple_appointments):
        """测试按医生姓名查询"""
        appointments = test_db.query(Appointment).filter(
            Appointment.doctor_name == "内科医生"
        ).all()
        assert len(appointments) == 1

    def test_appointment_update_status(self, test_db, create_appointment):
        """测试更新预约状态"""
        appointment = create_appointment(status="pending")

        appointment.status = "confirmed"
        test_db.commit()
        test_db.refresh(appointment)

        assert appointment.status == "confirmed"

    def test_appointment_with_notes(self, test_db):
        """测试带备注的预约"""
        appointment = Appointment(
            patient_name="患者",
            doctor_name="医生",
            appointment_time=datetime(2025, 12, 20, 10, 0, 0),
            reason="定期复查",
            notes="请空腹检查"
        )
        test_db.add(appointment)
        test_db.commit()
        test_db.refresh(appointment)

        assert appointment.reason == "定期复查"
        assert appointment.notes == "请空腹检查"


class TestModelRelationships:
    """模型关系测试（注意：当前实现使用字符串关联而非外键）"""

    def test_patient_name_in_appointments(self, test_db, create_patient, create_appointment):
        """测试患者姓名在预约中的使用"""
        patient = create_patient(name="关系测试患者")
        appointment = create_appointment(patient_name=patient.name)

        # 查询该患者的所有预约（通过姓名）
        appointments = test_db.query(Appointment).filter(
            Appointment.patient_name == patient.name
        ).all()

        assert len(appointments) == 1
        assert appointments[0].patient_name == patient.name

    def test_doctor_name_in_appointments(self, test_db, create_doctor, create_appointment):
        """测试医生姓名在预约中的使用"""
        doctor = create_doctor(name="关系测试医生")
        appointment = create_appointment(doctor_name=doctor.name)

        # 查询该医生的所有预约（通过姓名）
        appointments = test_db.query(Appointment).filter(
            Appointment.doctor_name == doctor.name
        ).all()

        assert len(appointments) == 1
        assert appointments[0].doctor_name == doctor.name

    def test_orphan_appointment_issue(self, test_db, create_patient, create_appointment):
        """测试孤儿预约问题 - 当前设计的缺陷"""
        patient = create_patient(name="将被删除的患者")
        appointment = create_appointment(patient_name=patient.name)

        # 删除患者
        test_db.delete(patient)
        test_db.commit()

        # 预约仍然存在（孤儿记录） - 这是设计缺陷
        orphan_appointment = test_db.query(Appointment).filter(
            Appointment.patient_name == "将被删除的患者"
        ).first()

        assert orphan_appointment is not None  # 孤儿预约仍然存在
        # 注意: 这个测试展示了当前设计的问题，应该使用外键约束来避免
