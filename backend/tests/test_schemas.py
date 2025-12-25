"""
Pydantic Schema 验证测试
测试数据验证、枚举约束、自定义验证器
"""
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from schemas import (
    PatientCreate, PatientUpdate, Patient,
    DoctorCreate, DoctorUpdate, Doctor,
    AppointmentCreate, AppointmentUpdate, Appointment,
    GenderEnum, SpecialtyEnum, DoctorStatusEnum, AppointmentStatusEnum
)


class TestPatientSchemas:
    """患者 Schema 测试"""

    def test_patient_create_valid(self, sample_patient_data):
        """测试有效的患者创建数据"""
        patient = PatientCreate(**sample_patient_data)

        assert patient.name == "张三"
        assert patient.age == 35
        assert patient.gender == GenderEnum.male
        assert patient.phone == "13800138000"
        assert patient.medical_condition == "感冒发烧"

    def test_patient_create_required_fields_only(self):
        """测试仅包含必填字段"""
        patient = PatientCreate(
            name="李四",
            age=25,
            gender=GenderEnum.female,
            medical_condition="体检"
        )

        assert patient.name == "李四"
        assert patient.phone is None
        assert patient.address is None

    def test_patient_create_missing_required_field(self):
        """测试缺少必填字段"""
        with pytest.raises(ValidationError) as exc_info:
            PatientCreate(
                name="王五",
                age=30
                # 缺少 gender 和 medical_condition
            )

        errors = exc_info.value.errors()
        error_fields = [error['loc'][0] for error in errors]
        assert 'gender' in error_fields
        assert 'medical_condition' in error_fields

    def test_patient_age_validation_minimum(self):
        """测试年龄最小值验证"""
        # 有效: 0岁
        patient = PatientCreate(
            name="新生儿",
            age=0,
            gender=GenderEnum.male,
            medical_condition="出生检查"
        )
        assert patient.age == 0

        # 无效: 负数
        with pytest.raises(ValidationError) as exc_info:
            PatientCreate(
                name="无效",
                age=-1,
                gender=GenderEnum.male,
                medical_condition="测试"
            )

        assert 'age' in str(exc_info.value)

    def test_patient_age_validation_maximum(self):
        """测试年龄最大值验证"""
        # 有效: 150岁
        patient = PatientCreate(
            name="长寿老人",
            age=150,
            gender=GenderEnum.female,
            medical_condition="常规检查"
        )
        assert patient.age == 150

        # 无效: 超过150岁
        with pytest.raises(ValidationError) as exc_info:
            PatientCreate(
                name="无效",
                age=151,
                gender=GenderEnum.male,
                medical_condition="测试"
            )

        assert 'age' in str(exc_info.value)

    def test_patient_gender_enum_validation(self):
        """测试性别枚举验证"""
        # 有效的枚举值
        patient_male = PatientCreate(
            name="男性患者",
            age=30,
            gender="男",
            medical_condition="测试"
        )
        assert patient_male.gender == GenderEnum.male

        # 无效的枚举值
        with pytest.raises(ValidationError) as exc_info:
            PatientCreate(
                name="无效性别",
                age=30,
                gender="未知",
                medical_condition="测试"
            )

        assert 'gender' in str(exc_info.value)

    def test_patient_name_max_length(self):
        """测试姓名最大长度"""
        # 100个字符 - 有效
        long_name = "张" * 100
        patient = PatientCreate(
            name=long_name,
            age=30,
            gender=GenderEnum.male,
            medical_condition="测试"
        )
        assert len(patient.name) == 100

        # 超过100个字符 - 无效
        too_long_name = "张" * 101
        with pytest.raises(ValidationError):
            PatientCreate(
                name=too_long_name,
                age=30,
                gender=GenderEnum.male,
                medical_condition="测试"
            )

    def test_patient_update_schema(self):
        """测试患者更新 Schema"""
        update_data = PatientUpdate(
            name="更新姓名",
            age=40,
            gender=GenderEnum.female,
            medical_condition="更新病情",
            notes="更新备注"
        )

        assert update_data.name == "更新姓名"
        assert update_data.age == 40


class TestDoctorSchemas:
    """医生 Schema 测试"""

    def test_doctor_create_valid(self, sample_doctor_data):
        """测试有效的医生创建数据"""
        doctor = DoctorCreate(**sample_doctor_data)

        assert doctor.name == "李医生"
        assert doctor.specialty == SpecialtyEnum.internal_medicine
        assert doctor.experience == "10年"
        assert doctor.status == DoctorStatusEnum.on_duty

    def test_doctor_specialty_enum_validation(self):
        """测试专业科室枚举验证"""
        specialties = ["内科", "外科", "儿科", "妇产科", "眼科", "口腔科"]

        for specialty in specialties:
            doctor = DoctorCreate(
                name="测试医生",
                specialty=specialty,
                experience="5年"
            )
            assert doctor.specialty.value == specialty

        # 无效的专业科室
        with pytest.raises(ValidationError):
            DoctorCreate(
                name="测试医生",
                specialty="神经科",
                experience="5年"
            )

    def test_doctor_status_enum_validation(self):
        """测试医生状态枚举验证"""
        statuses = ["在职", "休息中", "离职"]

        for status in statuses:
            doctor = DoctorCreate(
                name="测试医生",
                specialty=SpecialtyEnum.internal_medicine,
                experience="5年",
                status=status
            )
            assert doctor.status.value == status

        # 无效的状态
        with pytest.raises(ValidationError):
            DoctorCreate(
                name="测试医生",
                specialty=SpecialtyEnum.internal_medicine,
                experience="5年",
                status="请假中"
            )

    def test_doctor_status_default_value(self):
        """测试医生状态默认值"""
        doctor = DoctorCreate(
            name="新医生",
            specialty=SpecialtyEnum.surgery,
            experience="3年"
        )

        assert doctor.status == DoctorStatusEnum.on_duty

    def test_doctor_missing_required_fields(self):
        """测试缺少必填字段"""
        with pytest.raises(ValidationError) as exc_info:
            DoctorCreate(
                name="测试医生"
                # 缺少 specialty 和 experience
            )

        errors = exc_info.value.errors()
        error_fields = [error['loc'][0] for error in errors]
        assert 'specialty' in error_fields
        assert 'experience' in error_fields

    def test_doctor_update_schema(self):
        """测试医生更新 Schema"""
        update_data = DoctorUpdate(
            name="更新姓名",
            specialty=SpecialtyEnum.pediatrics,
            experience="15年",
            status=DoctorStatusEnum.on_leave,
            notes="主任医师"
        )

        assert update_data.specialty == SpecialtyEnum.pediatrics
        assert update_data.status == DoctorStatusEnum.on_leave


class TestAppointmentSchemas:
    """预约 Schema 测试"""

    def test_appointment_create_valid(self):
        """测试有效的预约创建数据"""
        future_time = datetime.now() + timedelta(days=1)
        appointment = AppointmentCreate(
            patient_name="张三",
            doctor_name="李医生",
            appointment_time=future_time,
            status=AppointmentStatusEnum.pending,
            reason="定期复查"
        )

        assert appointment.patient_name == "张三"
        assert appointment.doctor_name == "李医生"
        assert appointment.status == AppointmentStatusEnum.pending

    def test_appointment_time_validation_future(self):
        """测试预约时间必须是未来时间（创建时）"""
        # 未来时间 - 有效
        future_time = datetime.now() + timedelta(hours=1)
        appointment = AppointmentCreate(
            patient_name="患者",
            doctor_name="医生",
            appointment_time=future_time
        )
        assert appointment.appointment_time > datetime.now()

        # 过去时间 - 无效
        past_time = datetime.now() - timedelta(hours=1)
        with pytest.raises(ValidationError) as exc_info:
            AppointmentCreate(
                patient_name="患者",
                doctor_name="医生",
                appointment_time=past_time
            )

        assert '预约时间必须是未来的时间' in str(exc_info.value)

    def test_appointment_update_allows_past_time(self):
        """测试更新预约时允许过去时间"""
        # 编辑时允许过去时间
        past_time = datetime.now() - timedelta(hours=1)
        appointment = AppointmentUpdate(
            patient_name="患者",
            doctor_name="医生",
            appointment_time=past_time
        )

        # 不应抛出异常
        assert appointment.appointment_time < datetime.now()

    def test_appointment_status_enum_validation(self):
        """测试预约状态枚举验证"""
        future_time = datetime.now() + timedelta(days=1)
        statuses = ["pending", "confirmed", "cancelled"]

        for status in statuses:
            appointment = AppointmentCreate(
                patient_name="患者",
                doctor_name="医生",
                appointment_time=future_time,
                status=status
            )
            assert appointment.status.value == status

        # 无效的状态
        with pytest.raises(ValidationError):
            AppointmentCreate(
                patient_name="患者",
                doctor_name="医生",
                appointment_time=future_time,
                status="completed"
            )

    def test_appointment_status_default_value(self):
        """测试预约状态默认值"""
        future_time = datetime.now() + timedelta(days=1)
        appointment = AppointmentCreate(
            patient_name="患者",
            doctor_name="医生",
            appointment_time=future_time
        )

        assert appointment.status == AppointmentStatusEnum.pending

    def test_appointment_missing_required_fields(self):
        """测试缺少必填字段"""
        with pytest.raises(ValidationError) as exc_info:
            AppointmentCreate(
                patient_name="患者"
                # 缺少 doctor_name 和 appointment_time
            )

        errors = exc_info.value.errors()
        error_fields = [error['loc'][0] for error in errors]
        assert 'doctor_name' in error_fields
        assert 'appointment_time' in error_fields

    def test_appointment_with_optional_fields(self):
        """测试包含可选字段的预约"""
        future_time = datetime.now() + timedelta(days=1)
        appointment = AppointmentCreate(
            patient_name="患者",
            doctor_name="医生",
            appointment_time=future_time,
            reason="定期体检",
            notes="请空腹"
        )

        assert appointment.reason == "定期体检"
        assert appointment.notes == "请空腹"


class TestEnumValues:
    """枚举值测试"""

    def test_gender_enum_values(self):
        """测试性别枚举值"""
        assert GenderEnum.male.value == "男"
        assert GenderEnum.female.value == "女"
        assert len(GenderEnum) == 2

    def test_specialty_enum_values(self):
        """测试专业科室枚举值"""
        expected_specialties = {
            "internal_medicine": "内科",
            "surgery": "外科",
            "pediatrics": "儿科",
            "gynecology": "妇产科",
            "ophthalmology": "眼科",
            "dentistry": "口腔科"
        }

        for name, value in expected_specialties.items():
            assert SpecialtyEnum[name].value == value

        assert len(SpecialtyEnum) == 6

    def test_doctor_status_enum_values(self):
        """测试医生状态枚举值"""
        assert DoctorStatusEnum.on_duty.value == "在职"
        assert DoctorStatusEnum.on_leave.value == "休息中"
        assert DoctorStatusEnum.resigned.value == "离职"
        assert len(DoctorStatusEnum) == 3

    def test_appointment_status_enum_values(self):
        """测试预约状态枚举值"""
        assert AppointmentStatusEnum.pending.value == "pending"
        assert AppointmentStatusEnum.confirmed.value == "confirmed"
        assert AppointmentStatusEnum.cancelled.value == "cancelled"
        assert len(AppointmentStatusEnum) == 3


class TestSchemaTimestamps:
    """时间戳字段测试"""

    def test_patient_response_includes_timestamps(self, create_patient):
        """测试患者响应包含时间戳"""
        db_patient = create_patient(name="时间戳测试")

        # 转换为 Pydantic 模型
        patient_schema = Patient.model_validate(db_patient)

        assert hasattr(patient_schema, 'created_at')
        assert hasattr(patient_schema, 'updated_at')
        assert patient_schema.created_at is not None
        assert patient_schema.updated_at is not None

    def test_doctor_response_includes_timestamps(self, create_doctor):
        """测试医生响应包含时间戳"""
        db_doctor = create_doctor(name="时间戳测试")

        # 转换为 Pydantic 模型
        doctor_schema = Doctor.model_validate(db_doctor)

        assert hasattr(doctor_schema, 'created_at')
        assert hasattr(doctor_schema, 'updated_at')

    def test_appointment_response_includes_timestamps(self, create_appointment):
        """测试预约响应包含时间戳"""
        db_appointment = create_appointment()

        # 转换为 Pydantic 模型
        appointment_schema = Appointment.model_validate(db_appointment)

        assert hasattr(appointment_schema, 'created_at')
        assert hasattr(appointment_schema, 'updated_at')


class TestDataTypeConversion:
    """数据类型转换测试"""

    def test_age_integer_conversion(self):
        """测试年龄整数转换"""
        # 字符串数字应该被转换
        patient = PatientCreate(
            name="测试",
            age="30",  # 字符串
            gender=GenderEnum.male,
            medical_condition="测试"
        )
        assert patient.age == 30
        assert isinstance(patient.age, int)

    def test_datetime_string_conversion(self):
        """测试日期时间字符串转换"""
        future_time = (datetime.now() + timedelta(days=1)).isoformat()

        appointment = AppointmentCreate(
            patient_name="患者",
            doctor_name="医生",
            appointment_time=future_time  # ISO格式字符串
        )

        assert isinstance(appointment.appointment_time, datetime)

    def test_enum_string_conversion(self):
        """测试枚举字符串转换"""
        patient = PatientCreate(
            name="测试",
            age=30,
            gender="男",  # 字符串
            medical_condition="测试"
        )

        assert patient.gender == GenderEnum.male
        assert isinstance(patient.gender, GenderEnum)
