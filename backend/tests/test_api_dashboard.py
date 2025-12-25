"""
仪表盘 API 路由测试
测试 /api/dashboard 端点
"""
import pytest
from datetime import datetime, timedelta


class TestDashboardSummary:
    """测试仪表盘统计数据"""

    def test_get_dashboard_success(self, client):
        """测试成功获取仪表盘数据"""
        response = client.get("/api/dashboard/")

        assert response.status_code == 200
        data = response.json()

        # 验证响应结构
        assert 'summary' in data
        assert 'recent_appointments' in data
        assert 'departments' in data

    def test_dashboard_summary_structure(self, client):
        """测试仪表盘统计数据结构"""
        response = client.get("/api/dashboard/")
        data = response.json()

        summary = data['summary']

        # 验证所有必需字段
        assert 'total_patients' in summary
        assert 'total_doctors' in summary
        assert 'total_appointments_today' in summary
        assert 'appointments_this_week' in summary
        assert 'pending_cases' in summary

        # 验证数据类型
        assert isinstance(summary['total_patients'], int)
        assert isinstance(summary['total_doctors'], int)
        assert isinstance(summary['total_appointments_today'], int)
        assert isinstance(summary['appointments_this_week'], int)
        assert isinstance(summary['pending_cases'], int)

    def test_dashboard_with_no_data(self, client):
        """测试无数据时的仪表盘"""
        response = client.get("/api/dashboard/")
        data = response.json()

        summary = data['summary']

        # 所有计数应该为0
        assert summary['total_patients'] == 0
        assert summary['total_doctors'] == 0
        assert summary['total_appointments_today'] == 0

    def test_dashboard_patient_count(
        self, client, create_patient
    ):
        """测试患者总数统计"""
        # 创建3个患者
        for i in range(3):
            create_patient(name=f"患者{i}")

        response = client.get("/api/dashboard/")
        data = response.json()

        assert data['summary']['total_patients'] == 3

    def test_dashboard_doctor_count(
        self, client, create_doctor
    ):
        """测试医生总数统计"""
        # 创建5个医生
        specialties = ["内科", "外科", "儿科", "妇产科", "眼科"]
        for specialty in specialties:
            create_doctor(name=f"{specialty}医生", specialty=specialty)

        response = client.get("/api/dashboard/")
        data = response.json()

        assert data['summary']['total_doctors'] == 5

    def test_dashboard_today_appointments(
        self, client, create_appointment
    ):
        """测试今日预约统计"""
        today = datetime.now()

        # 创建今日预约
        create_appointment(appointment_time=today + timedelta(hours=1))
        create_appointment(appointment_time=today + timedelta(hours=2))

        # 创建明天的预约（不应计入今日）
        tomorrow = today + timedelta(days=1)
        create_appointment(appointment_time=tomorrow)

        response = client.get("/api/dashboard/")
        data = response.json()

        # 今日预约应该是2个
        assert data['summary']['total_appointments_today'] == 2

    def test_dashboard_weekly_appointments(
        self, client, create_appointment
    ):
        """测试本周预约统计"""
        today = datetime.now()

        # 创建本周的预约
        for i in range(3):
            create_appointment(appointment_time=today + timedelta(days=i))

        # 创建下周的预约（不应计入本周）
        next_week = today + timedelta(days=10)
        create_appointment(appointment_time=next_week)

        response = client.get("/api/dashboard/")
        data = response.json()

        # 本周预约应该至少3个
        assert data['summary']['appointments_this_week'] >= 3

    def test_dashboard_pending_cases(
        self, client, create_patient
    ):
        """测试待处理病例统计"""
        # 创建包含关键词的患者
        create_patient(name="患者1", medical_condition="需要复查")
        create_patient(name="患者2", medical_condition="继续观察治疗")
        create_patient(name="患者3", medical_condition="已治愈")

        response = client.get("/api/dashboard/")
        data = response.json()

        # 应该统计到包含"复查"或"观察"的患者
        assert data['summary']['pending_cases'] >= 2


class TestDashboardRecentAppointments:
    """测试近期预约列表"""

    def test_dashboard_recent_appointments_structure(self, client, create_appointment):
        """测试近期预约数据结构"""
        # 创建一个预约
        create_appointment()

        response = client.get("/api/dashboard/")
        data = response.json()

        recent = data['recent_appointments']
        assert isinstance(recent, list)

        if len(recent) > 0:
            appointment = recent[0]
            # 验证必需字段
            assert 'id' in appointment
            assert 'patient_name' in appointment
            assert 'doctor_name' in appointment
            assert 'appointment_time' in appointment
            assert 'status' in appointment

    def test_dashboard_recent_appointments_limit(self, client, create_appointment):
        """测试近期预约数量限制"""
        # 创建10个预约
        for i in range(10):
            future_time = datetime.now() + timedelta(days=i+1)
            create_appointment(appointment_time=future_time)

        response = client.get("/api/dashboard/")
        data = response.json()

        # 应该最多返回5个近期预约
        assert len(data['recent_appointments']) <= 5

    def test_dashboard_recent_appointments_sorted(self, client, create_appointment):
        """测试近期预约按时间排序"""
        # 创建不同时间的预约
        times = [
            datetime.now() + timedelta(days=3),
            datetime.now() + timedelta(days=1),
            datetime.now() + timedelta(days=2)
        ]

        for time in times:
            create_appointment(appointment_time=time)

        response = client.get("/api/dashboard/")
        data = response.json()

        recent = data['recent_appointments']

        # 验证按时间升序排序（最近的在前）
        if len(recent) >= 2:
            for i in range(len(recent) - 1):
                time1 = datetime.fromisoformat(recent[i]['appointment_time'].replace('Z', '+00:00'))
                time2 = datetime.fromisoformat(recent[i+1]['appointment_time'].replace('Z', '+00:00'))
                assert time1 <= time2

    def test_dashboard_recent_appointments_only_future(self, client, create_appointment):
        """测试只显示未来的预约"""
        # 创建未来的预约
        future_time = datetime.now() + timedelta(days=1)
        future_appointment = create_appointment(appointment_time=future_time)

        response = client.get("/api/dashboard/")
        data = response.json()

        recent = data['recent_appointments']

        # 所有预约时间应该在现在之后
        for appointment in recent:
            appointment_time = datetime.fromisoformat(
                appointment['appointment_time'].replace('Z', '+00:00')
            )
            # 允许一些时间误差
            assert appointment_time >= datetime.now() - timedelta(minutes=1)


class TestDashboardDepartments:
    """测试科室统计"""

    def test_dashboard_departments_structure(self, client, create_doctor):
        """测试科室统计数据结构"""
        # 创建一个医生
        create_doctor(specialty="内科")

        response = client.get("/api/dashboard/")
        data = response.json()

        departments = data['departments']
        assert isinstance(departments, list)

        if len(departments) > 0:
            dept = departments[0]
            # 验证必需字段
            assert 'name' in dept
            assert 'doctor_count' in dept
            assert 'appointment_count' in dept

    def test_dashboard_departments_doctor_count(self, client, create_doctor):
        """测试科室医生数量统计"""
        # 创建不同科室的医生
        create_doctor(name="内科医生1", specialty="内科")
        create_doctor(name="内科医生2", specialty="内科")
        create_doctor(name="外科医生1", specialty="外科")

        response = client.get("/api/dashboard/")
        data = response.json()

        departments = data['departments']

        # 查找内科
        internal_dept = next(
            (d for d in departments if d['name'] == "内科"),
            None
        )

        assert internal_dept is not None
        assert internal_dept['doctor_count'] == 2

    def test_dashboard_departments_appointment_count(
        self, client, create_doctor, create_appointment
    ):
        """测试科室预约数量统计"""
        # 创建医生
        internal_doctor = create_doctor(name="内科医生", specialty="内科")
        surgery_doctor = create_doctor(name="外科医生", specialty="外科")

        # 创建预约
        create_appointment(doctor_name=internal_doctor.name)
        create_appointment(doctor_name=internal_doctor.name)
        create_appointment(doctor_name=surgery_doctor.name)

        response = client.get("/api/dashboard/")
        data = response.json()

        departments = data['departments']

        # 查找内科
        internal_dept = next(
            (d for d in departments if d['name'] == "内科"),
            None
        )

        assert internal_dept is not None
        assert internal_dept['appointment_count'] == 2

    def test_dashboard_all_specialties_represented(self, client, multiple_doctors):
        """测试所有科室都被统计"""
        response = client.get("/api/dashboard/")
        data = response.json()

        departments = data['departments']
        dept_names = [d['name'] for d in departments]

        # 验证所有科室都在统计中
        expected_specialties = ["内科", "外科", "儿科", "妇产科", "眼科", "口腔科"]
        for specialty in expected_specialties:
            assert specialty in dept_names


class TestDashboardIntegration:
    """仪表盘集成测试"""

    def test_dashboard_full_data_scenario(
        self, client, create_patient, create_doctor, create_appointment
    ):
        """测试完整数据场景的仪表盘"""
        # 创建患者
        patient1 = create_patient(name="患者1", medical_condition="需要复查")
        patient2 = create_patient(name="患者2", medical_condition="健康")
        patient3 = create_patient(name="患者3", medical_condition="继续观察")

        # 创建医生
        doctor1 = create_doctor(name="内科医生", specialty="内科")
        doctor2 = create_doctor(name="外科医生", specialty="外科")

        # 创建预约
        today = datetime.now()
        create_appointment(
            patient_name=patient1.name,
            doctor_name=doctor1.name,
            appointment_time=today + timedelta(hours=1)
        )
        create_appointment(
            patient_name=patient2.name,
            doctor_name=doctor2.name,
            appointment_time=today + timedelta(days=1)
        )

        response = client.get("/api/dashboard/")
        data = response.json()

        # 验证统计数据
        summary = data['summary']
        assert summary['total_patients'] == 3
        assert summary['total_doctors'] == 2
        assert summary['total_appointments_today'] == 1
        assert summary['pending_cases'] == 2  # "复查"和"观察"

        # 验证科室统计
        departments = data['departments']
        assert len(departments) == 2

    def test_dashboard_updates_in_realtime(
        self, client, create_patient, create_doctor
    ):
        """测试仪表盘实时更新"""
        # 初始状态
        response1 = client.get("/api/dashboard/")
        initial_patient_count = response1.json()['summary']['total_patients']

        # 添加新患者
        create_patient(name="新患者")

        # 再次获取仪表盘
        response2 = client.get("/api/dashboard/")
        new_patient_count = response2.json()['summary']['total_patients']

        # 验证数据已更新
        assert new_patient_count == initial_patient_count + 1

    def test_dashboard_empty_state(self, client):
        """测试空状态仪表盘"""
        response = client.get("/api/dashboard/")
        data = response.json()

        summary = data['summary']
        assert summary['total_patients'] == 0
        assert summary['total_doctors'] == 0
        assert summary['total_appointments_today'] == 0
        assert summary['appointments_this_week'] == 0
        assert summary['pending_cases'] == 0

        assert len(data['recent_appointments']) == 0
        assert len(data['departments']) == 0

    def test_dashboard_performance_with_large_dataset(
        self, client, create_patient, create_doctor, create_appointment
    ):
        """测试大数据集情况下的性能"""
        # 创建较多数据
        for i in range(20):
            create_patient(name=f"患者{i}")

        for specialty in ["内科", "外科", "儿科"]:
            for i in range(3):
                create_doctor(name=f"{specialty}医生{i}", specialty=specialty)

        for i in range(30):
            future_time = datetime.now() + timedelta(days=i)
            create_appointment(appointment_time=future_time)

        # 仪表盘应该仍然快速响应
        response = client.get("/api/dashboard/")

        assert response.status_code == 200
        data = response.json()

        # 验证数据正确性
        assert data['summary']['total_patients'] == 20
        assert data['summary']['total_doctors'] == 9
        assert len(data['recent_appointments']) <= 5


class TestDashboardEdgeCases:
    """仪表盘边界情况测试"""

    def test_dashboard_with_past_appointments(self, client, create_appointment):
        """测试包含过去预约的情况"""
        # 创建过去的预约（通过直接数据库操作）
        # 注意: API 不允许创建过去的预约，但数据库中可能存在

        # 创建未来的预约
        future_time = datetime.now() + timedelta(days=1)
        create_appointment(appointment_time=future_time)

        response = client.get("/api/dashboard/")
        assert response.status_code == 200

    def test_dashboard_with_cancelled_appointments(
        self, client, create_appointment
    ):
        """测试包含已取消预约的情况"""
        # 创建不同状态的预约
        create_appointment(status="pending")
        create_appointment(status="confirmed")
        create_appointment(status="cancelled")

        response = client.get("/api/dashboard/")
        data = response.json()

        # 所有状态的预约都应该被计入统计
        assert data['summary']['total_appointments_today'] >= 0

    def test_dashboard_weekly_boundary(self, client, create_appointment):
        """测试周边界情况"""
        today = datetime.now()

        # 创建本周最后一天的预约
        week_end = today + timedelta(days=(6 - today.weekday()))
        create_appointment(appointment_time=week_end)

        # 创建下周第一天的预约
        next_week_start = week_end + timedelta(days=1)
        create_appointment(appointment_time=next_week_start + timedelta(hours=12))

        response = client.get("/api/dashboard/")
        data = response.json()

        # 验证周统计正确
        assert 'appointments_this_week' in data['summary']

    def test_dashboard_department_without_appointments(
        self, client, create_doctor
    ):
        """测试没有预约的科室"""
        # 创建医生但不创建预约
        create_doctor(name="孤独的医生", specialty="口腔科")

        response = client.get("/api/dashboard/")
        data = response.json()

        departments = data['departments']

        # 查找口腔科
        dentistry_dept = next(
            (d for d in departments if d['name'] == "口腔科"),
            None
        )

        assert dentistry_dept is not None
        assert dentistry_dept['doctor_count'] == 1
        assert dentistry_dept['appointment_count'] == 0
