# HospitalRun

HospitalRun 是一个现代化的医院管理系统，提供完整的患者管理、医生管理和预约管理功能。前后端分离架构，支持多语言国际化，具有完整的管理后台。

## ✨ 功能特性

### 🏥 核心功能
- **患者管理**: 完整的患者信息录入、查询、修改和删除
- **医生管理**: 多科室医生信息管理及其状态维护
- **预约管理**: 智能预约系统，支持状态跟踪和时间管理
- **统计仪表盘**: 实时统计数据展示和管理概览

### 🛠️ 技术架构
- **后端**: FastAPI + SQLAlchemy + MySQL/PostgreSQL
- **前端**: React + Material-UI + React Router
- **测试**: 完整的 unittest suite (pytest)
- **多语言**: 中文、日文、英文支持

### 🎯 适用场景
- 中小型医院诊所管理系统
- 医疗预约系统
- 患者管理平台

## 🚀 快速开始

### 环境要求

- **后端**:
  - Python 3.8+
  - MySQL 5.7+ 或 PostgreSQL 12+
- **前端**:
  - Node.js 16+
  - npm 7+

### 后端设置

1. **安装依赖**
   ```bash
   cd hospital/backend
   pip install -r requirements.txt
   ```

2. **设置数据库**

   支持 MySQL 或 PostgreSQL，请选择其一：

   - **MySQL**:
     ```sql
     CREATE DATABASE hospital_management
       DEFAULT CHARACTER SET utf8mb4
       DEFAULT COLLATE utf8mb4_unicode_ci;
     ```

   - **PostgreSQL**:
     ```sql
     CREATE DATABASE hospital_management
       WITH ENCODING 'UTF8'
       LC_COLLATE = 'zh_CN.UTF-8'
       LC_CTYPE = 'zh_CN.UTF-8';
     ```

3. **配置数据库连接**

   在 `backend/` 目录下创建 `.env` 文件：

   ```env
   # MySQL 配置
   DATABASE_URL=mysql+mysqlconnector://user:password@localhost:3306/hospital_management

   # 或 PostgreSQL 配置
   DATABASE_URL=postgresql://user:password@localhost:5432/hospital_management
   ```

4. **运行后端服务器**
   ```bash
   cd hospital/backend
   python main.py
   ```

   API 服务器将在 http://127.0.0.1:8000 启动
   - API 文档: http://127.0.0.1:8000/docs
   - 健康检查: http://127.0.0.1:8000/health

### 前端设置

1. **安装依赖**
   ```bash
   cd hospital
   npm install
   ```

2. **启动前端服务器**
   ```bash
   npm start
   ```

   前端应用将在 http://localhost:3000 启动

### 数据库初始化

系统会在首次启动时自动创建数据库表。也可以手动执行：

```bash
# 查看完整 DDL
cat hospital/DATABASE_DDL.md
```

## 📚 使用指南

### 主要页面

- **仪表盘**: 医院运营统计和概览
- **患者管理**: 患者信息的增删改查
- **医生管理**: 医生信息的增删改查
- **预约管理**: 预约记录的管理和状态跟踪

### API 接口

系统提供完整的 RESTful API，所有接口都返回统一的 JSON 响应格式。

**核心接口：**

#### 患者管理
```
GET    /api/patients          # 获取患者列表 (支持分页、搜索)
POST   /api/patients          # 创建患者
GET    /api/patients/{id}     # 获取患者详情
PUT    /api/patients/{id}     # 更新患者信息
DELETE /api/patients/{id}     # 删除患者
```

#### 医生管理
```
GET    /api/doctors           # 获取医生列表 (支持科室、状态筛选)
POST   /api/doctors           # 创建医生
GET    /api/doctors/{id}      # 获取医生详情
PUT    /api/doctors/{id}      # 更新医生信息
DELETE /api/doctors/{id}      # 删除医生
```

#### 预约管理
```
GET    /api/appointments      # 获取预约列表 (支持日期范围筛选)
POST   /api/appointments      # 创建预约
GET    /api/appointments/{id} # 获取预约详情
PUT    /api/appointments/{id} # 更新预约
DELETE /api/appointments/{id} # 删除预约
```

#### 统计概览
```
GET    /api/dashboard         # 获取系统统计数据
```

### API 使用示例

创建患者：
```bash
curl -X POST "http://127.0.0.1:8000/api/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "age": 35,
    "gender": "男",
    "phone": "13800138001",
    "medical_condition": "感冒发烧"
  }'
```

获取预约列表：
```bash
curl "http://127.0.0.1:8000/api/appointments?date_from=2024-12-01"
```

**完整API规范**: 查看 [`hospital/HospitalRun_API_JSON_规范.md`](hospital/HospitalRun_API_JSON_规范.md) 了解详细的请求/响应格式和业务规则。

## 🧪 测试

### 后端测试

```bash
cd hospital/backend

# 运行所有测试
pytest

# 使用测试脚本（推荐）
bash test.sh

# 生成覆盖率报告
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### 前端测试

```bash
cd hospital

# 运行React测试
npm test

# 生成覆盖率报告
npm test -- --coverage --watchAll=false
```

## 🌐 国际化

系统支持三种语言：

- **中文** (zh): 默认语言
- **英文** (en): 英文界面
- **日文** (ja): 日文界面

语言文件位于 `hospital/public/locales/`

## 📁 项目结构

```
hospital/
├── backend/                  # 后端代码
│   ├── main.py              # FastAPI 应用入口
│   ├── database.py          # 数据库配置
│   ├── models.py            # SQLAlchemy 模型
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # 数据库操作
│   ├── routes/              # API 路由
│   │   ├── patients.py      # 患者路由
│   │   ├── doctors.py       # 医生路由
│   │   ├── appointments.py  # 预约路由
│   │   └── dashboard.py     # 仪表盘路由
│   ├── tests/               # 测试套件
│   └── requirements.txt     # Python 依赖
├── src/                     # 前端代码
│   ├── components/          # React 组件
│   ├── pages/               # 页面组件
│   ├── services/            # API 服务
│   ├── contexts/            # React Context
│   └── App.js               # 应用入口
├── public/                  # 静态资源
└── DATABASE_DDL.md          # 数据库设计文档
```

## 🛠️ 开发工具

### 可用的 npm 脚本

```bash
# 启动开发服务器
npm start

# 构建生产版本
npm run build

# 运行测试
npm test

# 弹出配置文件（不可逆）
npm run eject
```

### 后端开发

```bash
# 热重载开发（后端）
cd hospital/backend
python main.py

# 使用 uvicorn 开发服务器
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## 📊 数据库设计

详细的数据库设计文档：`hospital/DATABASE_DDL.md`

### 核心数据模型

- **patients**: 患者表 - 基本信息、病情记录
- **doctors**: 医生表 - 个人信息、专业科室、工作状态
- **appointments**: 预约表 - 预约记录、状态跟踪

支持 MySQL 和 PostgreSQL 双引擎部署。

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 技术支持

- 📧 **Email**: support@hospitalrun.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/hospitalrun/hospitalrun/issues)
- 📖 **文档**: [完整文档](https://hospitalrun.com/docs)
- 💬 **讨论**: [GitHub Discussions](https://github.com/hospitalrun/hospitalrun/discussions)

## 🔄 更新日志

### v1.0.0 (2024-12-10)
- ✨ 初始发布
- 🏥 完整的医院管理系统
- 🌐 支持多语言（中英日）
- 🧪 完整的测试套件
- 📱 响应式前端界面

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 高性能 Web 框架
- [React](https://reactjs.org/) - 用户界面库
- [Material-UI](https://mui.com/) - React 组件库
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python ORM
