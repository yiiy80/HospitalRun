"""
患者 API 路由测试
测试 /api/patients 相关的所有端点
"""
import pytest
from datetime import datetime


class TestPatientCreate:
    """测试创建患者 API"""

    def test_create_patient_success(self, client, sample_patient_data):
        """测试成功创建患者"""
        response = client.post("/api/patients/", json=sample_patient_data)

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['message'] == "患者创建成功"
        assert data['data']['name'] == "张三"
        assert data['data']['age'] == 35
        assert data['data']['id'] is not None

    def test_create_patient_minimal_fields(self, client):
        """测试仅包含必填字段创建患者"""
        minimal_data = {
            "name": "最小字段测试",
            "age": 25,
            "gender": "女",
            "medical_condition": "体检"
        }

        response = client.post("/api/patients/", json=minimal_data)

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    def test_create_patient_missing_required_field(self, client):
        """测试缺少必填字段"""
        invalid_data = {
            "name": "测试",
            "age": 30
            # 缺少 gender 和 medical_condition
        }

        response = client.post("/api/patients/", json=invalid_data)

        assert response.status_code == 422  # Validation Error

    def test_create_patient_invalid_age(self, client):
        """测试无效的年龄值"""
        invalid_data = {
            "name": "测试",
            "age": -1,  # 负数年龄
            "gender": "男",
            "medical_condition": "测试"
        }

        response = client.post("/api/patients/", json=invalid_data)

        assert response.status_code == 422

    def test_create_patient_invalid_gender(self, client):
        """测试无效的性别值"""
        invalid_data = {
            "name": "测试",
            "age": 30,
            "gender": "未知",  # 无效的性别
            "medical_condition": "测试"
        }

        response = client.post("/api/patients/", json=invalid_data)

        assert response.status_code == 422

    def test_create_patient_with_all_optional_fields(self, client):
        """测试包含所有可选字段"""
        full_data = {
            "name": "完整数据",
            "age": 40,
            "gender": "男",
            "phone": "13900139000",
            "address": "上海市浦东新区",
            "medical_condition": "高血压",
            "notes": "需要定期复查"
        }

        response = client.post("/api/patients/", json=full_data)

        assert response.status_code == 200
        data = response.json()
        assert data['data']['phone'] == "13900139000"
        assert data['data']['address'] == "上海市浦东新区"
        assert data['data']['notes'] == "需要定期复查"


class TestPatientRead:
    """测试读取患者 API"""

    def test_get_patient_by_id_success(self, client, create_patient):
        """测试成功获取患者详情"""
        patient = create_patient(name="详情测试")

        response = client.get(f"/api/patients/{patient.id}")

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['data']['id'] == patient.id
        assert data['data']['name'] == "详情测试"

    def test_get_patient_by_id_not_found(self, client):
        """测试获取不存在的患者"""
        response = client.get("/api/patients/99999")

        assert response.status_code == 404
        data = response.json()
        assert "患者不存在" in data['detail']

    def test_get_patients_list_default(self, client, multiple_patients):
        """测试获取患者列表 - 默认参数"""
        response = client.get("/api/patients/")

        assert response.status_code == 200
        data = response.json()

        assert 'patients' in data
        assert 'pagination' in data
        assert len(data['patients']) == 5

    def test_get_patients_list_with_pagination(self, client, multiple_patients):
        """测试患者列表分页"""
        # 第一页
        response_page1 = client.get("/api/patients/?page=1&limit=2")
        data_page1 = response_page1.json()

        assert len(data_page1['patients']) == 2
        assert data_page1['pagination']['page'] == 1
        assert data_page1['pagination']['limit'] == 2
        assert data_page1['pagination']['total'] == 5
        assert data_page1['pagination']['totalPages'] == 3

        # 第二页
        response_page2 = client.get("/api/patients/?page=2&limit=2")
        data_page2 = response_page2.json()

        assert len(data_page2['patients']) == 2
        assert data_page2['pagination']['page'] == 2

    def test_get_patients_search_by_name(self, client, multiple_patients):
        """测试按姓名搜索患者"""
        response = client.get("/api/patients/?search=患者1")

        assert response.status_code == 200
        data = response.json()

        assert len(data['patients']) == 1
        assert data['patients'][0]['name'] == "患者1"

    def test_get_patients_filter_by_gender(self, client, multiple_patients):
        """测试按性别筛选患者"""
        # 男性患者
        response_male = client.get("/api/patients/?gender=男")
        data_male = response_male.json()
        assert len(data_male['patients']) == 3

        # 女性患者
        response_female = client.get("/api/patients/?gender=女")
        data_female = response_female.json()
        assert len(data_female['patients']) == 2

    def test_get_patients_search_and_filter_combined(self, client, create_patient):
        """测试搜索和筛选组合使用"""
        create_patient(name="张三", gender="男")
        create_patient(name="张四", gender="女")
        create_patient(name="李五", gender="男")

        response = client.get("/api/patients/?search=张&gender=男")
        data = response.json()

        assert len(data['patients']) == 1
        assert data['patients'][0]['name'] == "张三"

    def test_get_patients_empty_result(self, client):
        """测试空结果"""
        response = client.get("/api/patients/?search=不存在的患者")

        assert response.status_code == 200
        data = response.json()
        assert len(data['patients']) == 0
        assert data['pagination']['total'] == 0


class TestPatientUpdate:
    """测试更新患者 API"""

    def test_update_patient_success(self, client, create_patient):
        """测试成功更新患者"""
        patient = create_patient(name="原始姓名", age=30)

        update_data = {
            "name": "更新姓名",
            "age": 35,
            "gender": "男",
            "medical_condition": "更新病情",
            "notes": "新增备注"
        }

        response = client.put(f"/api/patients/{patient.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['message'] == "患者信息更新成功"
        assert data['data']['name'] == "更新姓名"
        assert data['data']['age'] == 35
        assert data['data']['notes'] == "新增备注"

    def test_update_patient_not_found(self, client):
        """测试更新不存在的患者"""
        update_data = {
            "name": "测试",
            "age": 30,
            "gender": "男",
            "medical_condition": "测试"
        }

        response = client.put("/api/patients/99999", json=update_data)

        assert response.status_code == 404
        data = response.json()
        assert "患者不存在" in data['detail']

    def test_update_patient_invalid_data(self, client, create_patient):
        """测试使用无效数据更新患者"""
        patient = create_patient(name="测试")

        invalid_data = {
            "name": "测试",
            "age": 200,  # 超过最大年龄
            "gender": "男",
            "medical_condition": "测试"
        }

        response = client.put(f"/api/patients/{patient.id}", json=invalid_data)

        assert response.status_code == 422

    def test_update_patient_partial_fields(self, client, create_patient):
        """测试部分字段更新"""
        patient = create_patient(
            name="原始姓名",
            age=30,
            medical_condition="原始病情"
        )

        # 只更新部分字段
        update_data = {
            "name": "原始姓名",
            "age": 35,  # 只更新年龄
            "gender": "男",
            "medical_condition": "原始病情"
        }

        response = client.put(f"/api/patients/{patient.id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data['data']['age'] == 35
        assert data['data']['name'] == "原始姓名"


class TestPatientDelete:
    """测试删除患者 API"""

    def test_delete_patient_success(self, client, create_patient):
        """测试成功删除患者"""
        patient = create_patient(name="待删除患者")
        patient_id = patient.id

        response = client.delete(f"/api/patients/{patient_id}")

        assert response.status_code == 200
        data = response.json()

        assert data['success'] is True
        assert data['message'] == "患者删除成功"

        # 验证患者已删除
        get_response = client.get(f"/api/patients/{patient_id}")
        assert get_response.status_code == 404

    def test_delete_patient_not_found(self, client):
        """测试删除不存在的患者"""
        response = client.delete("/api/patients/99999")

        assert response.status_code == 404
        data = response.json()
        assert "患者不存在" in data['detail']

    def test_delete_patient_and_verify_list(self, client, create_patient):
        """测试删除患者后列表变化"""
        patient1 = create_patient(name="患者1")
        patient2 = create_patient(name="患者2")

        # 获取初始列表
        response_before = client.get("/api/patients/")
        count_before = response_before.json()['pagination']['total']

        # 删除一个患者
        client.delete(f"/api/patients/{patient1.id}")

        # 再次获取列表
        response_after = client.get("/api/patients/")
        count_after = response_after.json()['pagination']['total']

        assert count_after == count_before - 1


class TestPatientAPIIntegration:
    """患者 API 集成测试"""

    def test_full_crud_workflow(self, client):
        """测试完整的 CRUD 流程"""
        # 1. 创建患者
        create_data = {
            "name": "集成测试患者",
            "age": 30,
            "gender": "男",
            "medical_condition": "初诊",
            "phone": "13800138000"
        }

        create_response = client.post("/api/patients/", json=create_data)
        assert create_response.status_code == 200
        patient_id = create_response.json()['data']['id']

        # 2. 读取患者
        read_response = client.get(f"/api/patients/{patient_id}")
        assert read_response.status_code == 200
        assert read_response.json()['data']['name'] == "集成测试患者"

        # 3. 更新患者
        update_data = {
            "name": "集成测试患者",
            "age": 31,
            "gender": "男",
            "medical_condition": "复诊",
            "phone": "13800138000"
        }

        update_response = client.put(f"/api/patients/{patient_id}", json=update_data)
        assert update_response.status_code == 200
        assert update_response.json()['data']['age'] == 31
        assert update_response.json()['data']['medical_condition'] == "复诊"

        # 4. 删除患者
        delete_response = client.delete(f"/api/patients/{patient_id}")
        assert delete_response.status_code == 200

        # 5. 验证删除
        get_deleted_response = client.get(f"/api/patients/{patient_id}")
        assert get_deleted_response.status_code == 404

    def test_create_multiple_patients_and_search(self, client):
        """测试创建多个患者并搜索"""
        patients_data = [
            {"name": "王小明", "age": 25, "gender": "男", "medical_condition": "感冒"},
            {"name": "王小红", "age": 30, "gender": "女", "medical_condition": "发烧"},
            {"name": "李小华", "age": 35, "gender": "男", "medical_condition": "咳嗽"}
        ]

        # 创建患者
        for data in patients_data:
            response = client.post("/api/patients/", json=data)
            assert response.status_code == 200

        # 搜索姓王的患者
        search_response = client.get("/api/patients/?search=王")
        data = search_response.json()
        assert len(data['patients']) == 2

        # 筛选男性患者
        filter_response = client.get("/api/patients/?gender=男")
        data = filter_response.json()
        assert len(data['patients']) == 2

    def test_pagination_consistency(self, client):
        """测试分页一致性"""
        # 创建10个患者
        for i in range(10):
            client.post("/api/patients/", json={
                "name": f"分页测试{i}",
                "age": 20 + i,
                "gender": "男" if i % 2 == 0 else "女",
                "medical_condition": f"病情{i}"
            })

        # 获取所有患者（分页）
        all_patients = []
        for page in range(1, 6):  # 5页，每页2条
            response = client.get(f"/api/patients/?page={page}&limit=2")
            data = response.json()
            all_patients.extend(data['patients'])

        # 验证没有重复
        patient_ids = [p['id'] for p in all_patients]
        assert len(patient_ids) == len(set(patient_ids))


class TestPatientAPIErrorHandling:
    """患者 API 错误处理测试"""

    def test_invalid_patient_id_format(self, client):
        """测试无效的患者 ID 格式"""
        response = client.get("/api/patients/abc")

        assert response.status_code == 422  # Validation error

    def test_negative_pagination_parameters(self, client):
        """测试负数分页参数"""
        response = client.get("/api/patients/?page=-1&limit=-10")

        assert response.status_code == 422

    def test_exceed_max_limit(self, client):
        """测试超过最大 limit 值"""
        response = client.get("/api/patients/?limit=1000")

        # 根据 schemas.py 的验证规则，limit 最大为 100
        assert response.status_code == 422

    def test_create_patient_with_extra_fields(self, client):
        """测试包含额外字段的创建请求"""
        data_with_extra = {
            "name": "测试",
            "age": 30,
            "gender": "男",
            "medical_condition": "测试",
            "extra_field": "这是多余的字段"  # Pydantic 会忽略
        }

        response = client.post("/api/patients/", json=data_with_extra)

        # Pydantic 默认会忽略额外字段
        assert response.status_code == 200

    def test_create_patient_empty_name(self, client):
        """测试空姓名"""
        invalid_data = {
            "name": "",  # 空姓名
            "age": 30,
            "gender": "男",
            "medical_condition": "测试"
        }

        response = client.post("/api/patients/", json=invalid_data)

        # Field 验证应该要求 name 不为空
        assert response.status_code in [400, 422]
