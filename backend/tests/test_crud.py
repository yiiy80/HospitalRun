"""
CRUD 操作测试
测试 crud.py 中的数据库操作函数
"""
import pytest
from datetime import datetime, timedelta
from crud import (
    # 患者 CRUD
    get_patient, get_patients, create_patient, update_patient, delete_patient,
    # 医生 CRUD
    get_doctor, get_doctors, create_doctor, update_doctor, delete_doctor,
    # 预约 CRUD
    get_appointment, get_appointments, create_appointment, update_appointment, delete_appointment,
    # Dashboard
    get_dashboard_summary
)
from schemas import (
    PatientCreate, PatientUpdate,
    DoctorCreate, DoctorUpdate,
    AppointmentCreate, AppointmentUpdate
)


class TestPatientCRUD:
    """患者 CRUD 操作测试"""

    def test_create_patient(self, test_db, sample_patient_data):
        """测试创建患者"""
        patient_schema = PatientCreate(**sample_patient_data)
        db_patient = create_patient(test_db, patient_schema)

        assert db_patient.id is not None
        assert db_patient.name == "张三"
        assert db_patient.age == 35
        assert db_patient.gender == "男"

    def test_get_patient_exists(self, test_db, create_patient):
        """测试获取存在的患者"""
        created_patient = create_patient(name="测试患者")

        fetched_patient = get_patient(test_db, created_patient.id)

        assert fetched_patient is not None
        assert fetched_patient.id == created_patient.id
        assert fetched_patient.name == "测试患者"

    def test_get_patient_not_exists(self, test_db):
        """测试获取不存在的患者"""
        patient = get_patient(test_db, 99999)
        assert patient is None

    def test_get_patients_no_filters(self, test_db, multiple_patients):
        """测试获取患者列表 - 无筛选"""
        patients, total = get_patients(test_db, skip=0, limit=10)

        assert len(patients) == 5
        assert total == 5

    def test_get_patients_pagination(self, test_db, multiple_patients):
        """测试患者列表分页"""
        # 第一页
        patients_page1, total = get_patients(test_db, skip=0, limit=2)
        assert len(patients_page1) == 2
        assert total == 5

        # 第二页
        patients_page2, total = get_patients(test_db, skip=2, limit=2)
        assert len(patients_page2) == 2

        # 确保不重复
        page1_ids = [p.id for p in patients_page1]
        page2_ids = [p.id for p in patients_page2]
        assert len(set(page1_ids) & set(page2_ids)) == 0

    def test_get_patients_search_by_name(self, test_db, multiple_patients):
        """测试按姓名搜索患者"""
        patients, total = get_patients(test_db, search="患者1")

        assert len(patients) == 1
        assert patients[0].name == "患者1"

    def test_get_patients_search_by_phone(self, test_db, multiple_patients):
        """测试按电话搜索患者"""
        patients, total = get_patients(test_db, search="13800138001")

        assert len(patients) == 1
        assert "13800138001" in patients[0].phone

    def test_get_patients_filter_by_gender(self, test_db, multiple_patients):
        """测试按性别筛选患者"""
        # 男性患者
        male_patients, total = get_patients(test_db, gender="男")
        assert len(male_patients) == 3

        # 女性患者
        female_patients, total = get_patients(test_db, gender="女")
        assert len(female_patients) == 2

    def test_update_patient(self, test_db, create_patient):
        """测试更新患者"""
        patient = create_patient(name="原始姓名", age=30)

        update_data = PatientUpdate(
            name="更新姓名",
            age=35,
            gender="男",
            medical_condition="更新病情"
        )

        updated_patient = update_patient(test_db, patient.id, update_data)

        assert updated_patient.name == "更新姓名"
        assert updated_patient.age == 35
        assert updated_patient.medical_condition == "更新病情"

    def test_update_patient_not_exists(self, test_db):
        """测试更新不存在的患者"""
        update_data = PatientUpdate(
            name="不存在",
            age=30,
            gender="男",
            medical_condition="测试"
        )

        result = update_patient(test_db, 99999, update_data)
        assert result is None

    def test_delete_patient_exists(self, test_db, create_patient):
        """测试删除存在的患者"""
        patient = create_patient(name="待删除")
        patient_id = patient.id

        result = delete_patient(test_db, patient_id)
        assert result is True

        # 验证已删除
        deleted = get_patient(test_db, patient_id)
        assert deleted is None

    def test_delete_patient_not_exists(self, test_db):
        """测试删除不存在的患者"""
        result = delete_patient(test_db, 99999)
        assert result is False


class TestDoctorCRUD:
    """医生 CRUD 操作测试"""

    def test_create_doctor(self, test_db, sample_doctor_data):
        """测试创建医生"""
        doctor_schema = DoctorCreate(**sample_doctor_data)
        db_doctor = create_doctor(test_db, doctor_schema)

        assert db_doctor.id is not None
        assert db_doctor.name == "李医生"
        assert db_doctor.specialty == "内科"
        assert db_doctor.status == "在职"

    def test_get_doctor_exists(self, test_db, create_doctor):
        """测试获取存在的医生"""
        created_doctor = create_doctor(name="测试医生")

        fetched_doctor = get_doctor(test_db, created_doctor.id)

        assert fetched_doctor is not None
        assert fetched_doctor.id == created_doctor.id
        assert fetched_doctor.name == "测试医生"

    def test_get_doctor_not_exists(self, test_db):
        """测试获取不存在的医生"""
        doctor = get_doctor(test_db, 99999)
        assert doctor is None

    def test_get_doctors_no_filters(self, test_db, multiple_doctors):
        """测试获取医生列表 - 无筛选"""
        doctors, summary = get_doctors(test_db)

        assert len(doctors) == 6
        assert summary['total'] == 6

    def test_get_doctors_filter_by_specialty(self, test_db, multiple_doctors):
        """测试按专业科室筛选医生"""
        # 注意: crud.py 中使用英文枚举名称
        doctors, summary = get_doctors(test_db, specialty="internal_medicine")

        assert len(doctors) == 1
        assert doctors[0].specialty == "内科"

    def test_get_doctors_filter_by_status(self, test_db, multiple_doctors):
        """测试按状态筛选医生"""
        doctors, summary = get_doctors(test_db, status="在职")

        assert len(doctors) == 6  # 所有医生都在职

    def test_get_doctors_search_by_name(self, test_db, multiple_doctors):
        """测试按姓名搜索医生"""
        doctors, summary = get_doctors(test_db, search="内科医生")

        assert len(doctors) == 1
        assert doctors[0].name == "内科医生"

    def test_get_doctors_summary_statistics(self, test_db, multiple_doctors):
        """测试医生统计信息"""
        doctors, summary = get_doctors(test_db)

        assert 'total' in summary
        assert 'specialty_count' in summary
        assert 'status_count' in summary

        # 每个专业应该有1个医生
        for specialty in ["内科", "外科", "儿科", "妇产科", "眼科", "口腔科"]:
            assert summary['specialty_count'].get(specialty) == 1

    def test_update_doctor(self, test_db, create_doctor):
        """测试更新医生"""
        doctor = create_doctor(name="原始姓名", status="在职")

        update_data = DoctorUpdate(
            name="更新姓名",
            specialty="外科",
            experience="15年",
            status="休息中"
        )

        updated_doctor = update_doctor(test_db, doctor.id, update_data)

        assert updated_doctor.name == "更新姓名"
        assert updated_doctor.specialty == "外科"
        assert updated_doctor.status == "休息中"

    def test_update_doctor_not_exists(self, test_db):
        """测试更新不存在的医生"""
        update_data = DoctorUpdate(
            name="不存在",
            specialty="内科",
            experience="5年"
        )

        result = update_doctor(test_db, 99999, update_data)
        assert result is None

    def test_delete_doctor_exists(self, test_db, create_doctor):
        """测试删除存在的医生"""
        doctor = create_doctor(name="待删除")
        doctor_id = doctor.id

        result = delete_doctor(test_db, doctor_id)
        assert result is True

        # 验证已删除
        deleted = get_doctor(test_db, doctor_id)
        assert deleted is None

    def test_delete_doctor_not_exists(self, test_db):
        """测试删除不存在的医生"""
        result = delete_doctor(test_db, 99999)
        assert result is False


class TestAppointmentCRUD:
    """预约 CRUD 操作测试"""

    def test_create_appointment(self, test_db):
        """测试创建预约"""
        future_time = datetime.now() + timedelta(days=1)
        appointment_schema = AppointmentCreate(
            patient_name="张三",
            doctor_name="李医生",
            appointment_time=future_time,
            reason="复查"
        )

        db_appointment = create_appointment(test_db, appointment_schema)

        assert db_appointment.id is not None
        assert db_appointment.patient_name == "张三"
        assert db_appointment.doctor_name == "李医生"
        assert db_appointment.status == "pending"

    def test_get_appointment_exists(self, test_db, create_appointment):
        """测试获取存在的预约"""
        created_appointment = create_appointment()

        fetched_appointment = get_appointment(test_db, created_appointment.id)

        assert fetched_appointment is not None
        assert fetched_appointment.id == created_appointment.id

    def test_get_appointment_not_exists(self, test_db):
        """测试获取不存在的预约"""
        appointment = get_appointment(test_db, 99999)
        assert appointment is None

    def test_get_appointments_no_filters(self, test_db, multiple_appointments):
        """测试获取预约列表 - 无筛选"""
        appointments, today_summary = get_appointments(test_db)

        assert len(appointments) == 3

    def test_get_appointments_filter_by_date_range(self, test_db, multiple_appointments):
        """测试按日期范围筛选预约"""
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)

        appointments, _ = get_appointments(
            test_db,
            date_from=tomorrow.strftime('%Y-%m-%d'),
            date_to=tomorrow.strftime('%Y-%m-%d')
        )

        # 至少应该有明天的预约
        assert len(appointments) >= 1

    def test_get_appointments_filter_by_status(self, test_db, create_appointment):
        """测试按状态筛选预约"""
        create_appointment(status="pending")
        create_appointment(status="confirmed")

        pending_appointments, _ = get_appointments(test_db, status="pending")
        confirmed_appointments, _ = get_appointments(test_db, status="confirmed")

        assert len(pending_appointments) >= 1
        assert len(confirmed_appointments) >= 1

    def test_get_appointments_filter_by_doctor(self, test_db, create_appointment):
        """测试按医生筛选预约"""
        create_appointment(doctor_name="张医生")
        create_appointment(doctor_name="李医生")

        zhang_appointments, _ = get_appointments(test_db, doctor="张医生")

        assert len(zhang_appointments) == 1
        assert zhang_appointments[0]['doctor_name'] == "张医生"

    def test_get_appointments_filter_by_patient(self, test_db, create_appointment):
        """测试按患者筛选预约"""
        create_appointment(patient_name="王五")
        create_appointment(patient_name="赵六")

        wang_appointments, _ = get_appointments(test_db, patient="王五")

        assert len(wang_appointments) == 1
        assert wang_appointments[0]['patient_name'] == "王五"

    def test_get_appointments_today_summary(self, test_db, create_appointment):
        """测试今日预约统计"""
        today = datetime.now()

        # 创建今日预约
        create_appointment(appointment_time=today + timedelta(hours=1), status="pending")
        create_appointment(appointment_time=today + timedelta(hours=2), status="confirmed")

        _, today_summary = get_appointments(test_db)

        assert 'total' in today_summary
        assert 'confirmed' in today_summary
        assert 'pending' in today_summary
        assert 'cancelled' in today_summary

    def test_get_appointments_with_patient_doctor_details(
        self, test_db, create_patient, create_doctor, create_appointment
    ):
        """测试预约包含患者和医生详细信息"""
        # 创建患者和医生
        patient = create_patient(name="详情测试患者")
        doctor = create_doctor(name="详情测试医生")

        # 创建预约
        appointment = create_appointment(
            patient_name=patient.name,
            doctor_name=doctor.name
        )

        # 获取预约列表
        appointments, _ = get_appointments(test_db)

        # 找到我们创建的预约
        our_appointment = next(
            (a for a in appointments if a['patient_name'] == patient.name),
            None
        )

        assert our_appointment is not None
        assert our_appointment['patient'] is not None
        assert our_appointment['doctor'] is not None
        assert our_appointment['patient']['name'] == patient.name
        assert our_appointment['doctor']['name'] == doctor.name

    def test_update_appointment(self, test_db, create_appointment):
        """测试更新预约"""
        appointment = create_appointment(status="pending")

        new_time = datetime.now() + timedelta(days=2)
        update_data = AppointmentUpdate(
            patient_name=appointment.patient_name,
            doctor_name=appointment.doctor_name,
            appointment_time=new_time,
            status="confirmed",
            notes="已确认"
        )

        updated_appointment = update_appointment(test_db, appointment.id, update_data)

        assert updated_appointment.status == "confirmed"
        assert updated_appointment.notes == "已确认"

    def test_update_appointment_not_exists(self, test_db):
        """测试更新不存在的预约"""
        update_data = AppointmentUpdate(
            patient_name="患者",
            doctor_name="医生",
            appointment_time=datetime.now() + timedelta(days=1)
        )

        result = update_appointment(test_db, 99999, update_data)
        assert result is None

    def test_delete_appointment_exists(self, test_db, create_appointment):
        """测试删除存在的预约"""
        appointment = create_appointment()
        appointment_id = appointment.id

        result = delete_appointment(test_db, appointment_id)
        assert result is True

        # 验证已删除
        deleted = get_appointment(test_db, appointment_id)
        assert deleted is None

    def test_delete_appointment_not_exists(self, test_db):
        """测试删除不存在的预约"""
        result = delete_appointment(test_db, 99999)
        assert result is False


class TestDashboardCRUD:
    """仪表盘统计测试"""

    def test_dashboard_summary_basic_counts(
        self, test_db, multiple_patients, multiple_doctors, multiple_appointments
    ):
        """测试基本统计数据"""
        dashboard_data = get_dashboard_summary(test_db)

        assert 'summary' in dashboard_data
        summary = dashboard_data['summary']

        assert summary['total_patients'] == 5
        assert summary['total_doctors'] == 6
        assert 'total_appointments_today' in summary
        assert 'appointments_this_week' in summary
        assert 'pending_cases' in summary

    def test_dashboard_recent_appointments(self, test_db, multiple_appointments):
        """测试近期预约列表"""
        dashboard_data = get_dashboard_summary(test_db)

        assert 'recent_appointments' in dashboard_data
        recent = dashboard_data['recent_appointments']

        assert len(recent) <= 5  # 最多5条
        assert isinstance(recent, list)

    def test_dashboard_departments_statistics(self, test_db, multiple_doctors):
        """测试科室统计"""
        dashboard_data = get_dashboard_summary(test_db)

        assert 'departments' in dashboard_data
        departments = dashboard_data['departments']

        assert len(departments) == 6  # 6个科室

        # 每个科室应该有统计信息
        for dept in departments:
            assert 'name' in dept
            assert 'doctor_count' in dept
            assert 'appointment_count' in dept

    def test_dashboard_pending_cases(self, test_db, create_patient):
        """测试待处理病例统计"""
        # 创建包含关键词的患者
        create_patient(medical_condition="需要复查")
        create_patient(medical_condition="继续观察")
        create_patient(medical_condition="正常")

        dashboard_data = get_dashboard_summary(test_db)
        summary = dashboard_data['summary']

        # 应该统计到包含"复查"或"观察"的患者
        assert summary['pending_cases'] >= 2

    def test_dashboard_weekly_appointments(self, test_db, create_appointment):
        """测试本周预约统计"""
        # 创建本周的预约
        today = datetime.now()
        week_appointment = create_appointment(
            appointment_time=today + timedelta(days=1)
        )

        # 创建下周的预约
        next_week_appointment = create_appointment(
            appointment_time=today + timedelta(days=10)
        )

        dashboard_data = get_dashboard_summary(test_db)
        summary = dashboard_data['summary']

        # 本周预约数应该包含今天和明天的
        assert summary['appointments_this_week'] >= 1


class TestCRUDEdgeCases:
    """CRUD 边界情况测试"""

    def test_search_with_special_characters(self, test_db, create_patient):
        """测试包含特殊字符的搜索"""
        create_patient(name="张三（VIP）")

        patients, total = get_patients(test_db, search="张三")
        assert len(patients) == 1

    def test_empty_search_returns_all(self, test_db, multiple_patients):
        """测试空搜索返回所有记录"""
        patients, total = get_patients(test_db, search="")
        assert total == 5

    def test_pagination_out_of_range(self, test_db, multiple_patients):
        """测试分页超出范围"""
        patients, total = get_patients(test_db, skip=100, limit=10)
        assert len(patients) == 0
        assert total == 5  # 总数不变

    def test_large_limit_value(self, test_db, multiple_patients):
        """测试大的 limit 值"""
        patients, total = get_patients(test_db, skip=0, limit=1000)
        assert len(patients) == 5
        assert total == 5
