"""
HospitalRun Backend 测试套件

这个包包含了 HospitalRun 后端 API 的完整测试套件。

测试模块:
- conftest.py: 测试配置和 fixtures
- test_models.py: 数据库模型测试
- test_schemas.py: Pydantic schema 验证测试
- test_crud.py: CRUD 操作测试
- test_api_patients.py: 患者 API 路由测试
- test_api_doctors.py: 医生 API 路由测试
- test_api_appointments.py: 预约 API 路由测试
- test_api_dashboard.py: 仪表盘 API 测试

运行测试:
    pytest                              # 运行所有测试
    pytest tests/test_models.py         # 运行特定模块
    pytest tests/ -v                    # 详细输出
    pytest --cov=. --cov-report=html    # 生成覆盖率报告
"""

__version__ = "1.0.0"
__author__ = "HospitalRun Team"
