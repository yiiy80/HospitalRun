"""
预约 API 路由测试
测试 /api/appointments 相关的所有端点
"""
import pytest
from datetime import datetime, timedelta


class TestAppointmentCreate:
    """测试创建预约 API"""

    def test_create_appointment_success(self, client):
        """测试成功创建预约"""
        future_time = datetime.now() + timedelta(days=1)
        appointment_data = {
            "patient_name": "张三",
            "doctor_name": "李医生",
            "appointment_time": future_time.isoformat(),
            "reason": "定期复查"
        }

        response = client.post("/api/appointments/", json=appointment_data)

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['message'] == "预约创建成功"
        assert data['data']['patient_name'] == "张三"
        assert data['data']['doctor_name'] == "李医生"
        assert data['data']['status'] == "pending"

    def test_create_appointment_past_time_fails(self, client):
        """测试创建过去时间的预约失败"""
        past_time = datetime.now() - timedelta(hours=1)
        appointment_data = {
            "patient_name": "患者",
            "doctor_name": "医生",
            "appointment_time": past_time.isoformat()
        }

        response = client.post("/api/appointments/", json=appointment_data)

        # 应该返回验证错误
        assert response.status_code in [400, 422]

    def test_create_appointment_missing_required_field(self, client):
        """测试缺少必填字段"""
        invalid_data = {
            "patient_name": "患者"
            # 缺少 doctor_name 和 appointment_time
        }

        response = client.post("/api/appointments/", json=invalid_data)

        assert response.status_code == 422

    def test_create_appointment_with_all_fields(self, client):
        """测试包含所有字段的预约创建"""
        future_time = datetime.now() + timedelta(days=2)
        appointment_data = {
            "patient_name": "王五",
            "doctor_name": "赵医生",
            "appointment_time": future_time.isoformat(),
            "status": "confirmed",
            "reason": "常规体检",
            "notes": "请空腹"
        }

        response = client.post("/api/appointments/", json=appointment_data)

        assert response.status_code == 200
        data = response.json()
        assert data['data']['status'] == "confirmed"
        assert data['data']['reason'] == "常规体检"
        assert data['data']['notes'] == "请空腹"

    def test_create_appointment_invalid_status(self, client):
        """测试无效的预约状态"""
        future_time = datetime.now() + timedelta(days=1)
        invalid_data = {
            "patient_name": "患者",
            "doctor_name": "医生",
            "appointment_time": future_time.isoformat(),
            "status": "completed"  # 无效的状态
        }

        response = client.post("/api/appointments/", json=invalid_data)

        assert response.status_code == 422


class TestAppointmentRead:
    """测试读取预约 API"""

    def test_get_appointment_by_id_success(self, client, create_appointment):
        """测试成功获取预约详情"""
        appointment = create_appointment()

        response = client.get(f"/api/appointments/{appointment.id}")

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['data']['id'] == appointment.id

    def test_get_appointment_by_id_not_found(self, client):
        """测试获取不存在的预约"""
        response = client.get("/api/appointments/99999")

        assert response.status_code == 404
        data = response.json()
        assert "预约不存在" in data['detail']

    def test_get_appointments_list_default(self, client, multiple_appointments):
        """测试获取预约列表 - 默认参数"""
        response = client.get("/api/appointments/")

        assert response.status_code == 200
        data = response.json()

        assert 'appointments' in data
        assert 'today_summary' in data
        assert len(data['appointments']) >= 3

    def test_get_appointments_filter_by_date_range(self, client, create_appointment):
        """测试按日期范围筛选预约"""
        tomorrow = datetime.now() + timedelta(days=1)
        day_after = datetime.now() + timedelta(days=2)

        # 创建明天和后天的预约
        create_appointment(appointment_time=tomorrow)
        create_appointment(appointment_time=day_after)

        # 筛选明天的预约
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        response = client.get(f"/api/appointments/?date_from={tomorrow_str}&date_to={tomorrow_str}")

        assert response.status_code == 200
        data = response.json()
        assert len(data['appointments']) >= 1

    def test_get_appointments_filter_by_status(self, client, create_appointment):
        """测试按状态筛选预约"""
        create_appointment(status="pending")
        create_appointment(status="confirmed")
        create_appointment(status="cancelled")

        # 筛选待确认的预约
        response = client.get("/api/appointments/?status=pending")
        data = response.json()

        for appointment in data['appointments']:
            assert appointment['status'] == "pending"

    def test_get_appointments_filter_by_doctor(self, client, create_appointment):
        """测试按医生筛选预约"""
        create_appointment(doctor_name="张医生")
        create_appointment(doctor_name="李医生")

        response = client.get("/api/appointments/?doctor=张医生")

        assert response.status_code == 200
        data = response.json()

        for appointment in data['appointments']:
            assert appointment['doctor_name'] == "张医生"

    def test_get_appointments_filter_by_patient(self, client, create_appointment):
        """测试按患者筛选预约"""
        create_appointment(patient_name="王五")
        create_appointment(patient_name="赵六")

        response = client.get("/api/appointments/?patient=王五")

        assert response.status_code == 200
        data = response.json()

        for appointment in data['appointments']:
            assert appointment['patient_name'] == "王五"

    def test_get_appointments_today_summary(self, client, create_appointment):
        """测试今日预约统计"""
        today = datetime.now()

        # 创建不同状态的今日预约
        create_appointment(appointment_time=today + timedelta(hours=1), status="pending")
        create_appointment(appointment_time=today + timedelta(hours=2), status="confirmed")

        response = client.get("/api/appointments/")
        data = response.json()

        summary = data['today_summary']
        assert 'total' in summary
        assert 'confirmed' in summary
        assert 'pending' in summary
        assert 'cancelled' in summary

    def test_get_appointments_with_patient_doctor_details(
        self, client, create_patient, create_doctor, create_appointment
    ):
        """测试预约列表包含患者和医生详细信息"""
        # 创建患者和医生
        patient = create_patient(name="详情患者", age=30, gender="男")
        doctor = create_doctor(name="详情医生", specialty="内科")

        # 创建预约
        create_appointment(patient_name=patient.name, doctor_name=doctor.name)

        response = client.get("/api/appointments/")
        data = response.json()

        # 找到对应的预约
        our_appointment = next(
            (a for a in data['appointments'] if a['patient_name'] == patient.name),
            None
        )

        assert our_appointment is not None
        assert our_appointment['patient'] is not None
        assert our_appointment['doctor'] is not None
        assert our_appointment['patient']['age'] == 30
        assert our_appointment['doctor']['specialty'] == "内科"


class TestAppointmentUpdate:
    """测试更新预约 API"""

    def test_update_appointment_success(self, client, create_appointment):
        """测试成功更新预约"""
        appointment = create_appointment(status="pending")

        new_time = datetime.now() + timedelta(days=3)
        update_data = {
            "patient_name": appointment.patient_name,
            "doctor_name": appointment.doctor_name,
            "appointment_time": new_time.isoformat(),
            "status": "confirmed",
            "notes": "已确认，请准时到达"
        }

        response = client.put(f"/api/appointments/{appointment.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['message'] == "预约更新成功"
        assert data['data']['status'] == "confirmed"
        assert data['data']['notes'] == "已确认，请准时到达"

    def test_update_appointment_allows_past_time(self, client, create_appointment):
        """测试更新预约时允许过去时间"""
        appointment = create_appointment()

        # 编辑时允许设置为过去时间
        past_time = datetime.now() - timedelta(hours=1)
        update_data = {
            "patient_name": appointment.patient_name,
            "doctor_name": appointment.doctor_name,
            "appointment_time": past_time.isoformat(),
            "status": "cancelled"
        }

        response = client.put(f"/api/appointments/{appointment.id}", json=update_data)

        # 更新应该成功（与创建不同）
        assert response.status_code == 200

    def test_update_appointment_not_found(self, client):
        """测试更新不存在的预约"""
        update_data = {
            "patient_name": "患者",
            "doctor_name": "医生",
            "appointment_time": (datetime.now() + timedelta(days=1)).isoformat()
        }

        response = client.put("/api/appointments/99999", json=update_data)

        assert response.status_code == 404
        data = response.json()
        assert "预约不存在" in data['detail']

    def test_update_appointment_status_change(self, client, create_appointment):
        """测试预约状态变更"""
        appointment = create_appointment(status="pending")

        # 状态变更: pending -> confirmed
        update_data = {
            "patient_name": appointment.patient_name,
            "doctor_name": appointment.doctor_name,
            "appointment_time": appointment.appointment_time.isoformat(),
            "status": "confirmed"
        }

        response = client.put(f"/api/appointments/{appointment.id}", json=update_data)
        assert response.json()['data']['status'] == "confirmed"

        # 状态变更: confirmed -> cancelled
        update_data['status'] = "cancelled"
        response = client.put(f"/api/appointments/{appointment.id}", json=update_data)
        assert response.json()['data']['status'] == "cancelled"


class TestAppointmentDelete:
    """测试删除预约 API"""

    def test_delete_appointment_success(self, client, create_appointment):
        """测试成功删除预约"""
        appointment = create_appointment()
        appointment_id = appointment.id

        response = client.delete(f"/api/appointments/{appointment_id}")

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['message'] == "预约删除成功"

        # 验证预约已删除
        get_response = client.get(f"/api/appointments/{appointment_id}")
        assert get_response.status_code == 404

    def test_delete_appointment_not_found(self, client):
        """测试删除不存在的预约"""
        response = client.delete("/api/appointments/99999")

        assert response.status_code == 404
        data = response.json()
        assert "预约不存在" in data['detail']


class TestAppointmentAPIIntegration:
    """预约 API 集成测试"""

    def test_full_crud_workflow(self, client):
        """测试完整的 CRUD 流程"""
        # 1. 创建预约
        future_time = datetime.now() + timedelta(days=1)
        create_data = {
            "patient_name": "集成测试患者",
            "doctor_name": "集成测试医生",
            "appointment_time": future_time.isoformat(),
            "reason": "初次就诊"
        }

        create_response = client.post("/api/appointments/", json=create_data)
        assert create_response.status_code == 200
        appointment_id = create_response.json()['data']['id']

        # 2. 读取预约
        read_response = client.get(f"/api/appointments/{appointment_id}")
        assert read_response.status_code == 200
        assert read_response.json()['data']['patient_name'] == "集成测试患者"

        # 3. 更新预约
        new_time = datetime.now() + timedelta(days=2)
        update_data = {
            "patient_name": "集成测试患者",
            "doctor_name": "集成测试医生",
            "appointment_time": new_time.isoformat(),
            "status": "confirmed",
            "reason": "复诊"
        }

        update_response = client.put(f"/api/appointments/{appointment_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()['data']['status'] == "confirmed"
        assert update_response.json()['data']['reason'] == "复诊"

        # 4. 删除预约
        delete_response = client.delete(f"/api/appointments/{appointment_id}")
        assert delete_response.status_code == 200

        # 5. 验证删除
        get_deleted_response = client.get(f"/api/appointments/{appointment_id}")
        assert get_deleted_response.status_code == 404

    def test_appointment_workflow_with_real_patient_doctor(
        self, client, create_patient, create_doctor
    ):
        """测试使用真实患者和医生创建预约的工作流"""
        # 1. 创建患者
        patient = create_patient(name="真实患者", age=35, gender="男")

        # 2. 创建医生
        doctor = create_doctor(name="真实医生", specialty="内科")

        # 3. 创建预约
        future_time = datetime.now() + timedelta(days=1)
        appointment_data = {
            "patient_name": patient.name,
            "doctor_name": doctor.name,
            "appointment_time": future_time.isoformat(),
            "reason": "健康检查"
        }

        create_response = client.post("/api/appointments/", json=appointment_data)
        assert create_response.status_code == 200

        # 4. 获取预约列表，验证包含详细信息
        list_response = client.get("/api/appointments/")
        data = list_response.json()

        our_appointment = next(
            (a for a in data['appointments'] if a['patient_name'] == patient.name),
            None
        )

        assert our_appointment is not None
        assert our_appointment['patient']['age'] == 35
        assert our_appointment['doctor']['specialty'] == "内科"

    def test_multiple_appointments_same_doctor(self, client, create_doctor):
        """测试同一医生的多个预约"""
        doctor = create_doctor(name="繁忙医生")

        # 创建3个预约
        for i in range(3):
            future_time = datetime.now() + timedelta(days=i+1, hours=10)
            client.post("/api/appointments/", json={
                "patient_name": f"患者{i+1}",
                "doctor_name": doctor.name,
                "appointment_time": future_time.isoformat()
            })

        # 筛选该医生的预约
        response = client.get(f"/api/appointments/?doctor={doctor.name}")
        data = response.json()

        assert len(data['appointments']) == 3

    def test_appointment_status_lifecycle(self, client, create_appointment):
        """测试预约状态生命周期"""
        appointment = create_appointment(status="pending")
        appointment_id = appointment.id

        # 阶段1: 待确认
        response = client.get(f"/api/appointments/{appointment_id}")
        assert response.json()['data']['status'] == "pending"

        # 阶段2: 确认
        client.put(f"/api/appointments/{appointment_id}", json={
            "patient_name": appointment.patient_name,
            "doctor_name": appointment.doctor_name,
            "appointment_time": appointment.appointment_time.isoformat(),
            "status": "confirmed"
        })

        response = client.get(f"/api/appointments/{appointment_id}")
        assert response.json()['data']['status'] == "confirmed"

        # 阶段3: 取消
        client.put(f"/api/appointments/{appointment_id}", json={
            "patient_name": appointment.patient_name,
            "doctor_name": appointment.doctor_name,
            "appointment_time": appointment.appointment_time.isoformat(),
            "status": "cancelled"
        })

        response = client.get(f"/api/appointments/{appointment_id}")
        assert response.json()['data']['status'] == "cancelled"


class TestAppointmentAPIEdgeCases:
    """预约 API 边界情况测试"""

    def test_appointment_exactly_now(self, client):
        """测试预约时间为当前时刻"""
        # 当前时间应该被认为是过去（创建时要求未来）
        now = datetime.now()
        appointment_data = {
            "patient_name": "患者",
            "doctor_name": "医生",
            "appointment_time": now.isoformat()
        }

        response = client.post("/api/appointments/", json=appointment_data)

        # 应该失败（要求未来时间）
        assert response.status_code in [400, 422]

    def test_appointment_far_future(self, client):
        """测试很远的未来预约"""
        far_future = datetime.now() + timedelta(days=365)  # 一年后
        appointment_data = {
            "patient_name": "患者",
            "doctor_name": "医生",
            "appointment_time": far_future.isoformat()
        }

        response = client.post("/api/appointments/", json=appointment_data)

        # 应该成功（没有最大时间限制）
        assert response.status_code == 200

    def test_filter_date_range_inclusive(self, client, create_appointment):
        """测试日期范围筛选的包含性"""
        target_date = datetime.now() + timedelta(days=5)

        # 创建目标日期的预约
        create_appointment(appointment_time=target_date)

        # 使用相同日期作为起止日期
        date_str = target_date.strftime('%Y-%m-%d')
        response = client.get(f"/api/appointments/?date_from={date_str}&date_to={date_str}")

        data = response.json()
        assert len(data['appointments']) >= 1

    def test_combined_filters(self, client, create_appointment):
        """测试组合筛选条件"""
        tomorrow = datetime.now() + timedelta(days=1)

        # 创建符合条件的预约
        create_appointment(
            patient_name="特定患者",
            doctor_name="特定医生",
            appointment_time=tomorrow,
            status="pending"
        )

        # 创建不符合条件的预约
        create_appointment(
            patient_name="其他患者",
            doctor_name="特定医生",
            appointment_time=tomorrow,
            status="confirmed"
        )

        # 组合筛选
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        response = client.get(
            f"/api/appointments/?doctor=特定医生&status=pending&date_from={tomorrow_str}"
        )

        data = response.json()
        assert len(data['appointments']) == 1
        assert data['appointments'][0]['patient_name'] == "特定患者"
