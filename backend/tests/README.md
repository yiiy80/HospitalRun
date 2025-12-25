# HospitalRun Backend 测试文档

## 📋 目录

- [测试套件概述](#测试套件概述)
- [测试环境配置](#测试环境配置)
- [运行测试](#运行测试)
- [测试模块说明](#测试模块说明)
- [测试覆盖率](#测试覆盖率)
- [编写新测试](#编写新测试)
- [常见问题](#常见问题)

---

## 测试套件概述

本测试套件为 HospitalRun 后端 API 提供全面的单元测试和集成测试，确保代码质量和功能正确性。

### 测试统计

- **总测试文件**: 8 个
- **测试覆盖模块**:
  - 数据库模型 (Models)
  - 数据验证 (Schemas)
  - CRUD 操作
  - API 路由 (患者、医生、预约、仪表盘)

### 技术栈

- **测试框架**: pytest 7.4.3
- **异步支持**: pytest-asyncio 0.21.1
- **HTTP 客户端**: httpx 0.25.2 (FastAPI TestClient)
- **覆盖率工具**: pytest-cov 4.1.0
- **测试数据**: faker 20.1.0

---

## 测试环境配置

### 1. 安装依赖

```bash
# 在 backend 目录下执行
pip install -r requirements.txt
```

### 2. 验证安装

```bash
python -c "import pytest, sqlalchemy, pydantic; print('✅ 测试依赖已安装')"
```

### 3. 数据库配置

测试使用 **SQLite 内存数据库**，无需额外配置。每个测试函数都会创建独立的数据库实例，测试间完全隔离。

---

## 运行测试

### 快速开始

```bash
# 运行所有测试
pytest

# 使用测试脚本（推荐）
bash test.sh
```

### 运行特定模块

```bash
# 数据库模型测试
pytest tests/test_models.py -v

# Pydantic Schema 验证测试
pytest tests/test_schemas.py -v

# CRUD 操作测试
pytest tests/test_crud.py -v

# 患者 API 测试
pytest tests/test_api_patients.py -v

# 医生 API 测试
pytest tests/test_api_doctors.py -v

# 预约 API 测试
pytest tests/test_api_appointments.py -v

# 仪表盘 API 测试
pytest tests/test_api_dashboard.py -v
```

### 运行特定测试类

```bash
# 运行患者创建测试
pytest tests/test_api_patients.py::TestPatientCreate -v

# 运行医生 CRUD 测试
pytest tests/test_crud.py::TestDoctorCRUD -v
```

### 运行单个测试函数

```bash
pytest tests/test_models.py::TestPatientModel::test_create_patient_with_required_fields -v
```

### 使用标记筛选

```bash
# 运行单元测试
pytest -m unit

# 运行集成测试
pytest -m integration

# 运行数据库相关测试
pytest -m database
```

---

## 测试模块说明

### conftest.py - 测试配置

提供测试所需的 fixtures 和配置。

**主要 Fixtures**:

| Fixture | 说明 | 作用域 |
|---------|------|--------|
| `test_engine` | 测试数据库引擎 | function |
| `test_db` | 测试数据库会话 | function |
| `client` | FastAPI 测试客户端 | function |
| `sample_patient_data` | 示例患者数据 | function |
| `sample_doctor_data` | 示例医生数据 | function |
| `sample_appointment_data` | 示例预约数据 | function |
| `create_patient` | 患者工厂函数 | function |
| `create_doctor` | 医生工厂函数 | function |
| `create_appointment` | 预约工厂函数 | function |
| `multiple_patients` | 批量患者数据 | function |
| `multiple_doctors` | 批量医生数据 | function |
| `multiple_appointments` | 批量预约数据 | function |

**使用示例**:

```python
def test_example(client, create_patient):
    # 使用工厂函数创建患者
    patient = create_patient(name="测试患者", age=30)

    # 使用测试客户端调用 API
    response = client.get(f"/api/patients/{patient.id}")
    assert response.status_code == 200
```

### test_models.py - 数据库模型测试

测试 SQLAlchemy 模型的创建、验证和关系。

**测试类**:
- `TestPatientModel`: 患者模型测试（15 个测试）
- `TestDoctorModel`: 医生模型测试（10 个测试）
- `TestAppointmentModel`: 预约模型测试（12 个测试）
- `TestModelRelationships`: 模型关系测试（3 个测试）

**覆盖场景**:
- ✅ 必填字段验证
- ✅ 可选字段处理
- ✅ 枚举约束验证
- ✅ 自动时间戳
- ✅ 数据查询
- ✅ 数据删除
- ⚠️ 孤儿记录问题演示

### test_schemas.py - Schema 验证测试

测试 Pydantic 数据验证模式。

**测试类**:
- `TestPatientSchemas`: 患者 Schema（9 个测试）
- `TestDoctorSchemas`: 医生 Schema（8 个测试）
- `TestAppointmentSchemas`: 预约 Schema（8 个测试）
- `TestEnumValues`: 枚举值测试（4 个测试）
- `TestSchemaTimestamps`: 时间戳字段测试（3 个测试）
- `TestDataTypeConversion`: 类型转换测试（3 个测试）

**覆盖场景**:
- ✅ 必填字段验证
- ✅ 字段类型验证
- ✅ 数值范围验证（如年龄 0-150）
- ✅ 字符串长度验证
- ✅ 枚举值验证
- ✅ 自定义验证器（预约时间）
- ✅ 数据类型转换

### test_crud.py - CRUD 操作测试

测试 crud.py 中的数据库操作函数。

**测试类**:
- `TestPatientCRUD`: 患者 CRUD（12 个测试）
- `TestDoctorCRUD`: 医生 CRUD（12 个测试）
- `TestAppointmentCRUD`: 预约 CRUD（15 个测试）
- `TestDashboardCRUD`: 仪表盘统计（4 个测试）
- `TestCRUDEdgeCases`: 边界情况（4 个测试）

**覆盖场景**:
- ✅ 创建记录
- ✅ 读取单条/列表
- ✅ 更新记录
- ✅ 删除记录
- ✅ 分页查询
- ✅ 搜索功能
- ✅ 筛选条件
- ✅ 统计聚合

### test_api_patients.py - 患者 API 测试

测试 /api/patients 相关的所有端点。

**测试类**:
- `TestPatientCreate`: 创建患者 API（6 个测试）
- `TestPatientRead`: 读取患者 API（9 个测试）
- `TestPatientUpdate`: 更新患者 API（4 个测试）
- `TestPatientDelete`: 删除患者 API（3 个测试）
- `TestPatientAPIIntegration`: 集成测试（3 个测试）
- `TestPatientAPIErrorHandling`: 错误处理（6 个测试）

**HTTP 状态码验证**:
- `200 OK`: 成功操作
- `404 Not Found`: 资源不存在
- `422 Unprocessable Entity`: 验证错误

### test_api_doctors.py - 医生 API 测试

测试 /api/doctors 相关的所有端点。

**测试类**:
- `TestDoctorCreate`: 创建医生 API（5 个测试）
- `TestDoctorRead`: 读取医生 API（6 个测试）
- `TestDoctorUpdate`: 更新医生 API（4 个测试）
- `TestDoctorDelete`: 删除医生 API（2 个测试）
- `TestDoctorAPIIntegration`: 集成测试（3 个测试）
- `TestDoctorAPIEdgeCases`: 边界情况（5 个测试）

**特殊测试**:
- ✅ 所有专业科室验证
- ✅ 医生状态转换
- ✅ 统计信息准确性

### test_api_appointments.py - 预约 API 测试

测试 /api/appointments 相关的所有端点。

**测试类**:
- `TestAppointmentCreate`: 创建预约 API（5 个测试）
- `TestAppointmentRead`: 读取预约 API（9 个测试）
- `TestAppointmentUpdate`: 更新预约 API（4 个测试）
- `TestAppointmentDelete`: 删除预约 API（2 个测试）
- `TestAppointmentAPIIntegration`: 集成测试（4 个测试）
- `TestAppointmentAPIEdgeCases`: 边界情况（4 个测试）

**核心验证**:
- ✅ 创建时强制未来时间
- ✅ 编辑时允许过去时间
- ✅ 包含患者/医生详细信息
- ✅ 今日预约统计
- ✅ 日期范围筛选

### test_api_dashboard.py - 仪表盘 API 测试

测试 /api/dashboard 统计端点。

**测试类**:
- `TestDashboardSummary`: 统计数据测试（7 个测试）
- `TestDashboardRecentAppointments`: 近期预约测试（4 个测试）
- `TestDashboardDepartments`: 科室统计测试（4 个测试）
- `TestDashboardIntegration`: 集成测试（4 个测试）
- `TestDashboardEdgeCases`: 边界情况（4 个测试）

**统计指标验证**:
- ✅ 患者总数
- ✅ 医生总数
- ✅ 今日预约数
- ✅ 本周预约数
- ✅ 待处理病例数
- ✅ 科室医生/预约统计

---

## 测试覆盖率

### 生成覆盖率报告

```bash
# 生成 HTML 报告
pytest --cov=. --cov-report=html

# 生成终端报告
pytest --cov=. --cov-report=term-missing

# 同时生成两种报告
pytest --cov=. --cov-report=html --cov-report=term-missing
```

### 查看报告

```bash
# HTML 报告（推荐）
# 报告生成在 htmlcov/index.html
start htmlcov/index.html    # Windows
open htmlcov/index.html     # macOS
xdg-open htmlcov/index.html # Linux
```

### 目标覆盖率

| 模块 | 当前覆盖率 | 目标覆盖率 |
|------|-----------|-----------|
| models.py | ~90% | 95% |
| schemas.py | ~95% | 98% |
| crud.py | ~85% | 90% |
| routes/*.py | ~80% | 90% |
| **总体** | **~85%** | **92%** |

---

## 编写新测试

### 测试文件命名

- 文件名必须以 `test_` 开头
- 测试类必须以 `Test` 开头
- 测试函数必须以 `test_` 开头

### 示例：添加新的 API 测试

```python
# tests/test_api_patients.py

class TestPatientNewFeature:
    """测试患者新功能"""

    def test_new_feature_success(self, client, create_patient):
        """测试新功能成功场景"""
        patient = create_patient(name="测试")

        response = client.post(
            f"/api/patients/{patient.id}/new-feature",
            json={"param": "value"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True

    def test_new_feature_validation(self, client):
        """测试新功能参数验证"""
        response = client.post(
            "/api/patients/1/new-feature",
            json={"invalid": "data"}
        )

        assert response.status_code == 422
```

### 使用 Fixtures

```python
def test_with_fixtures(
    client,               # FastAPI 测试客户端
    test_db,             # 数据库会话
    create_patient,       # 患者工厂
    sample_patient_data   # 示例数据
):
    # 使用工厂函数
    patient = create_patient(name="工厂患者")

    # 使用示例数据
    response = client.post("/api/patients/", json=sample_patient_data)

    # 直接访问数据库
    from models import Patient
    db_patient = test_db.query(Patient).first()
    assert db_patient is not None
```

### 测试 Markers

```python
import pytest

@pytest.mark.unit
def test_unit_test():
    """单元测试"""
    pass

@pytest.mark.integration
def test_integration_test():
    """集成测试"""
    pass

@pytest.mark.database
def test_database_test():
    """数据库测试"""
    pass

@pytest.mark.slow
def test_slow_test():
    """慢速测试"""
    pass
```

---

## 常见问题

### 1. 导入错误

**问题**: `ModuleNotFoundError: No module named 'models'`

**解决**:
```bash
# 确保在 backend 目录下运行测试
cd hospital/backend
pytest
```

### 2. 数据库连接错误

**问题**: 测试无法连接数据库

**解决**: 测试使用内存 SQLite，不需要 MySQL。如果仍有问题，检查 conftest.py 中的数据库配置。

### 3. Fixture 未找到

**问题**: `fixture 'create_patient' not found`

**解决**: 确保 conftest.py 存在于 tests 目录中，pytest 会自动加载。

### 4. 测试数据污染

**问题**: 测试之间互相影响

**解决**: 每个测试函数都使用独立的数据库会话（`scope="function"`），数据不会共享。

### 5. 异步测试问题

**问题**: `coroutine was never awaited`

**解决**:
```python
# 使用 pytest-asyncio
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### 6. 覆盖率报告缺失模块

**问题**: 某些文件未出现在覆盖率报告中

**解决**:
```bash
# 指定要覆盖的源代码目录
pytest --cov=. --cov-report=html --cov-config=.coveragerc
```

---

## 持续集成

### GitHub Actions 示例

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        cd hospital/backend
        pip install -r requirements.txt

    - name: Run tests
      run: |
        cd hospital/backend
        pytest --cov=. --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

---

## 最佳实践

### ✅ 推荐做法

1. **每个功能都写测试**: 新功能开发时同步编写测试
2. **测试命名清晰**: 测试名称应明确说明测试内容
3. **使用 Fixtures**: 复用测试数据和设置
4. **独立测试**: 每个测试独立运行，不依赖其他测试
5. **测试边界情况**: 不仅测试正常流程，也测试异常情况
6. **保持测试简单**: 一个测试只验证一个功能点

### ❌ 避免做法

1. **不要在测试间共享状态**: 使用 `scope="function"`
2. **不要跳过失败的测试**: 修复而不是 `@pytest.mark.skip`
3. **不要测试第三方库**: 只测试自己的代码
4. **不要硬编码 ID**: 使用工厂函数动态创建

---

## 贡献指南

### 添加新测试

1. 确定测试类别（models/schemas/crud/api）
2. 在相应文件中添加测试类
3. 编写清晰的测试函数
4. 运行测试确保通过
5. 检查覆盖率是否提升

### 测试 Review Checklist

- [ ] 测试名称清晰描述功能
- [ ] 使用 fixtures 复用代码
- [ ] 测试成功和失败场景
- [ ] 验证 HTTP 状态码
- [ ] 验证响应数据结构
- [ ] 测试边界情况
- [ ] 测试通过且覆盖率提升

---

## 联系支持

如有测试相关问题：

1. 查看本文档的常见问题部分
2. 查看 pytest 官方文档: https://docs.pytest.org/
3. 查看 FastAPI 测试文档: https://fastapi.tiangolo.com/tutorial/testing/
4. 提交 Issue 到项目仓库

---

**最后更新**: 2025-12-10
**维护者**: HospitalRun Backend Team
