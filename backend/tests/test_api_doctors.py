"""
医生 API 路由测试
测试 /api/doctors 相关的所有端点
"""
import pytest


class TestDoctorCreate:
    """测试创建医生 API"""

    def test_create_doctor_success(self, client, sample_doctor_data):
        """测试成功创建医生"""
        response = client.post("/api/doctors/", json=sample_doctor_data)

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['message'] == "医生创建成功"
        assert data['data']['name'] == "李医生"
        assert data['data']['specialty'] == "内科"
        assert data['data']['id'] is not None

    def test_create_doctor_minimal_fields(self, client):
        """测试仅包含必填字段创建医生"""
        minimal_data = {
            "name": "张医生",
            "specialty": "外科",
            "experience": "5年"
        }

        response = client.post("/api/doctors/", json=minimal_data)

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        assert data['data']['status'] == "在职"  # 默认状态

    def test_create_doctor_missing_required_field(self, client):
        """测试缺少必填字段"""
        invalid_data = {
            "name": "测试医生"
            # 缺少 specialty 和 experience
        }

        response = client.post("/api/doctors/", json=invalid_data)

        assert response.status_code == 422

    def test_create_doctor_invalid_specialty(self, client):
        """测试无效的专业科室"""
        invalid_data = {
            "name": "测试医生",
            "specialty": "神经科",  # 不在枚举列表中
            "experience": "10年"
        }

        response = client.post("/api/doctors/", json=invalid_data)

        assert response.status_code == 422

    def test_create_doctor_all_specialties(self, client):
        """测试所有有效的专业科室"""
        specialties = ["内科", "外科", "儿科", "妇产科", "眼科", "口腔科"]

        for specialty in specialties:
            data = {
                "name": f"{specialty}医生",
                "specialty": specialty,
                "experience": "5年"
            }

            response = client.post("/api/doctors/", json=data)
            assert response.status_code == 200


class TestDoctorRead:
    """测试读取医生 API"""

    def test_get_doctor_by_id_success(self, client, create_doctor):
        """测试成功获取医生详情"""
        doctor = create_doctor(name="详情测试医生")

        response = client.get(f"/api/doctors/{doctor.id}")

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['data']['id'] == doctor.id
        assert data['data']['name'] == "详情测试医生"

    def test_get_doctor_by_id_not_found(self, client):
        """测试获取不存在的医生"""
        response = client.get("/api/doctors/99999")

        assert response.status_code == 404
        data = response.json()
        assert "医生不存在" in data['detail']

    def test_get_doctors_list_default(self, client, multiple_doctors):
        """测试获取医生列表 - 默认参数"""
        response = client.get("/api/doctors/")

        assert response.status_code == 200
        data = response.json()

        assert 'doctors' in data
        assert 'summary' in data
        assert len(data['doctors']) == 6

    def test_get_doctors_filter_by_specialty(self, client, multiple_doctors):
        """测试按专业科室筛选"""
        response = client.get("/api/doctors/?specialty=internal_medicine")

        assert response.status_code == 200
        data = response.json()

        assert len(data['doctors']) == 1
        assert data['doctors'][0]['specialty'] == "内科"

    def test_get_doctors_filter_by_status(self, client, create_doctor):
        """测试按状态筛选"""
        create_doctor(name="在职医生", status="在职")
        create_doctor(name="休息医生", status="休息中")

        response_on_duty = client.get("/api/doctors/?status=在职")
        data_on_duty = response_on_duty.json()
        assert len(data_on_duty['doctors']) >= 1

        response_on_leave = client.get("/api/doctors/?status=休息中")
        data_on_leave = response_on_leave.json()
        assert len(data_on_leave['doctors']) >= 1

    def test_get_doctors_search_by_name(self, client, create_doctor):
        """测试按姓名搜索医生"""
        create_doctor(name="王小明")
        create_doctor(name="李小华")

        response = client.get("/api/doctors/?search=王")

        assert response.status_code == 200
        data = response.json()

        assert len(data['doctors']) == 1
        assert "王" in data['doctors'][0]['name']

    def test_get_doctors_summary_statistics(self, client, multiple_doctors):
        """测试医生列表返回统计信息"""
        response = client.get("/api/doctors/")

        assert response.status_code == 200
        data = response.json()

        summary = data['summary']
        assert 'total' in summary
        assert 'specialty_count' in summary
        assert 'status_count' in summary
        assert summary['total'] == 6


class TestDoctorUpdate:
    """测试更新医生 API"""

    def test_update_doctor_success(self, client, create_doctor):
        """测试成功更新医生"""
        doctor = create_doctor(name="原始姓名", specialty="内科")

        update_data = {
            "name": "更新姓名",
            "specialty": "外科",
            "experience": "15年",
            "status": "休息中",
            "notes": "主任医师"
        }

        response = client.put(f"/api/doctors/{doctor.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['message'] == "医生信息更新成功"
        assert data['data']['name'] == "更新姓名"
        assert data['data']['specialty'] == "外科"
        assert data['data']['status'] == "休息中"

    def test_update_doctor_not_found(self, client):
        """测试更新不存在的医生"""
        update_data = {
            "name": "测试",
            "specialty": "内科",
            "experience": "5年"
        }

        response = client.put("/api/doctors/99999", json=update_data)

        assert response.status_code == 404
        data = response.json()
        assert "医生不存在" in data['detail']

    def test_update_doctor_invalid_specialty(self, client, create_doctor):
        """测试更新为无效的专业科室"""
        doctor = create_doctor(name="测试医生")

        invalid_data = {
            "name": "测试医生",
            "specialty": "心理科",  # 无效的专业
            "experience": "5年"
        }

        response = client.put(f"/api/doctors/{doctor.id}", json=invalid_data)

        assert response.status_code == 422

    def test_update_doctor_status_change(self, client, create_doctor):
        """测试医生状态变更"""
        doctor = create_doctor(name="测试医生", status="在职")

        # 变更为休息中
        update_data = {
            "name": doctor.name,
            "specialty": doctor.specialty,
            "experience": doctor.experience,
            "status": "休息中"
        }

        response = client.put(f"/api/doctors/{doctor.id}", json=update_data)

        assert response.status_code == 200
        assert response.json()['data']['status'] == "休息中"


class TestDoctorDelete:
    """测试删除医生 API"""

    def test_delete_doctor_success(self, client, create_doctor):
        """测试成功删除医生"""
        doctor = create_doctor(name="待删除医生")
        doctor_id = doctor.id

        response = client.delete(f"/api/doctors/{doctor_id}")

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['message'] == "医生删除成功"

        # 验证医生已删除
        get_response = client.get(f"/api/doctors/{doctor_id}")
        assert get_response.status_code == 404

    def test_delete_doctor_not_found(self, client):
        """测试删除不存在的医生"""
        response = client.delete("/api/doctors/99999")

        assert response.status_code == 404
        data = response.json()
        assert "医生不存在" in data['detail']


class TestDoctorAPIIntegration:
    """医生 API 集成测试"""

    def test_full_crud_workflow(self, client):
        """测试完整的 CRUD 流程"""
        # 1. 创建医生
        create_data = {
            "name": "集成测试医生",
            "specialty": "儿科",
            "experience": "8年",
            "phone": "13900139000",
            "notes": "副主任医师"
        }

        create_response = client.post("/api/doctors/", json=create_data)
        assert create_response.status_code == 200
        doctor_id = create_response.json()['data']['id']

        # 2. 读取医生
        read_response = client.get(f"/api/doctors/{doctor_id}")
        assert read_response.status_code == 200
        assert read_response.json()['data']['name'] == "集成测试医生"

        # 3. 更新医生
        update_data = {
            "name": "集成测试医生",
            "specialty": "儿科",
            "experience": "10年",  # 更新工作经验
            "status": "在职",
            "notes": "主任医师"  # 更新职称
        }

        update_response = client.put(f"/api/doctors/{doctor_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()['data']['experience'] == "10年"
        assert update_response.json()['data']['notes'] == "主任医师"

        # 4. 删除医生
        delete_response = client.delete(f"/api/doctors/{doctor_id}")
        assert delete_response.status_code == 200

        # 5. 验证删除
        get_deleted_response = client.get(f"/api/doctors/{doctor_id}")
        assert get_deleted_response.status_code == 404

    def test_create_doctors_for_all_departments(self, client):
        """测试为所有科室创建医生"""
        specialties = ["内科", "外科", "儿科", "妇产科", "眼科", "口腔科"]

        created_doctors = []
        for specialty in specialties:
            data = {
                "name": f"{specialty}主任",
                "specialty": specialty,
                "experience": "15年"
            }

            response = client.post("/api/doctors/", json=data)
            assert response.status_code == 200
            created_doctors.append(response.json()['data'])

        # 验证所有医生创建成功
        list_response = client.get("/api/doctors/")
        doctors_list = list_response.json()['doctors']

        assert len(doctors_list) >= 6

        # 验证统计信息
        summary = list_response.json()['summary']
        for specialty in specialties:
            assert specialty in summary['specialty_count']

    def test_specialty_filter_accuracy(self, client):
        """测试专业科室筛选准确性"""
        # 创建不同科室的医生
        specialties_data = [
            ("内科医生1", "内科"),
            ("内科医生2", "内科"),
            ("外科医生1", "外科")
        ]

        for name, specialty in specialties_data:
            client.post("/api/doctors/", json={
                "name": name,
                "specialty": specialty,
                "experience": "5年"
            })

        # 筛选内科医生
        response = client.get("/api/doctors/?specialty=internal_medicine")
        data = response.json()

        # 验证只返回内科医生
        for doctor in data['doctors']:
            assert doctor['specialty'] == "内科"


class TestDoctorAPIEdgeCases:
    """医生 API 边界情况测试"""

    def test_create_doctor_with_very_long_name(self, client):
        """测试非常长的姓名"""
        long_name = "张" * 100  # 100个字符（最大长度）

        data = {
            "name": long_name,
            "specialty": "内科",
            "experience": "5年"
        }

        response = client.post("/api/doctors/", json=data)
        assert response.status_code == 200

        # 超过最大长度
        too_long_name = "张" * 101
        invalid_data = {
            "name": too_long_name,
            "specialty": "内科",
            "experience": "5年"
        }

        response = client.post("/api/doctors/", json=invalid_data)
        assert response.status_code == 422

    def test_search_with_partial_match(self, client, create_doctor):
        """测试部分匹配搜索"""
        create_doctor(name="王小明医生")
        create_doctor(name="王小华医生")
        create_doctor(name="李小明医生")

        # 搜索"王"应该匹配两个医生
        response = client.get("/api/doctors/?search=王")
        data = response.json()
        assert len(data['doctors']) == 2

        # 搜索"小明"应该匹配两个医生
        response = client.get("/api/doctors/?search=小明")
        data = response.json()
        assert len(data['doctors']) == 2

    def test_multiple_filters_combined(self, client, create_doctor):
        """测试多个筛选条件组合"""
        create_doctor(name="王医生", specialty="内科", status="在职")
        create_doctor(name="李医生", specialty="内科", status="休息中")
        create_doctor(name="张医生", specialty="外科", status="在职")

        # 筛选：内科 + 在职
        response = client.get("/api/doctors/?specialty=internal_medicine&status=在职")
        data = response.json()

        assert len(data['doctors']) == 1
        assert data['doctors'][0]['name'] == "王医生"

    def test_empty_result_search(self, client):
        """测试搜索无结果"""
        response = client.get("/api/doctors/?search=不存在的医生")

        assert response.status_code == 200
        data = response.json()
        assert len(data['doctors']) == 0
        assert data['summary']['total'] == 0

    def test_status_transitions(self, client, create_doctor):
        """测试医生状态转换"""
        doctor = create_doctor(name="状态测试医生", status="在职")
        doctor_id = doctor.id

        # 状态转换: 在职 -> 休息中
        update_data = {
            "name": "状态测试医生",
            "specialty": doctor.specialty,
            "experience": doctor.experience,
            "status": "休息中"
        }

        response = client.put(f"/api/doctors/{doctor_id}", json=update_data)
        assert response.json()['data']['status'] == "休息中"

        # 状态转换: 休息中 -> 离职
        update_data['status'] = "离职"
        response = client.put(f"/api/doctors/{doctor_id}", json=update_data)
        assert response.json()['data']['status'] == "离职"
