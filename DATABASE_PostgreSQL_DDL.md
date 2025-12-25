# 医院管理系统 - PostgreSQL DDL

## 数据模型概览

本系统包含三个核心实体：
- **患者 (Patients)** - 管理患者基本信息和病情
- **医生 (Doctors)** - 管理医生信息、专业和状态
- **预约 (Appointments)** - 管理患者与医生的预约记录

---

## PostgreSQL DDL

```sql
-- 创建数据库
CREATE DATABASE hospital_management
  WITH ENCODING 'UTF8'
  LC_COLLATE = 'zh_CN.UTF-8'
  LC_CTYPE = 'zh_CN.UTF-8';

\c hospital_management;

-- ============================================
-- 1. 患者表 (Patients)
-- ============================================
CREATE TABLE patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL CHECK (age > 0 AND age < 150),
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('男', '女')),
    phone VARCHAR(20),
    address TEXT,
    medical_condition TEXT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE patients IS '患者信息表';
COMMENT ON COLUMN patients.id IS '患者ID';
COMMENT ON COLUMN patients.name IS '患者姓名';
COMMENT ON COLUMN patients.age IS '年龄';
COMMENT ON COLUMN patients.gender IS '性别';
COMMENT ON COLUMN patients.phone IS '联系电话';
COMMENT ON COLUMN patients.address IS '家庭地址';
COMMENT ON COLUMN patients.medical_condition IS '病情描述';
COMMENT ON COLUMN patients.notes IS '备注信息';

CREATE INDEX idx_patients_name ON patients(name);
CREATE INDEX idx_patients_phone ON patients(phone);

-- ============================================
-- 2. 医生表 (Doctors)
-- ============================================
CREATE TABLE doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(50) NOT NULL CHECK (specialty IN ('内科', '外科', '儿科', '妇产科', '眼科', '口腔科')),
    experience VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT '在职' CHECK (status IN ('在职', '休息中', '离职')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE doctors IS '医生信息表';
COMMENT ON COLUMN doctors.id IS '医生ID';
COMMENT ON COLUMN doctors.name IS '医生姓名';
COMMENT ON COLUMN doctors.specialty IS '专业科室';
COMMENT ON COLUMN doctors.experience IS '工作经验（如：10年）';
COMMENT ON COLUMN doctors.phone IS '联系电话';
COMMENT ON COLUMN doctors.status IS '工作状态';
COMMENT ON COLUMN doctors.notes IS '备注信息（如：主任医师）';

CREATE INDEX idx_doctors_name ON doctors(name);
CREATE INDEX idx_doctors_specialty ON doctors(specialty);
CREATE INDEX idx_doctors_status ON doctors(status);

-- ============================================
-- 3. 预约表 (Appointments)
-- ============================================
CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    appointment_time TIMESTAMP NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled')),
    reason TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE appointments IS '预约记录表';
COMMENT ON COLUMN appointments.id IS '预约ID';
COMMENT ON COLUMN appointments.patient_name IS '患者姓名';
COMMENT ON COLUMN appointments.doctor_name IS '医生姓名';
COMMENT ON COLUMN appointments.appointment_time IS '预约时间';
COMMENT ON COLUMN appointments.status IS '预约状态：pending=待确认, confirmed=已确认, cancelled=已取消';
COMMENT ON COLUMN appointments.reason IS '预约原因';
COMMENT ON COLUMN appointments.notes IS '备注信息';

CREATE INDEX idx_appointments_patient_name ON appointments(patient_name);
CREATE INDEX idx_appointments_doctor_name ON appointments(doctor_name);
CREATE INDEX idx_appointments_time ON appointments(appointment_time);
CREATE INDEX idx_appointments_status ON appointments(status);

-- ============================================
-- 创建更新时间自动更新函数
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为每个表添加触发器
CREATE TRIGGER update_patients_updated_at BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_doctors_updated_at BEFORE UPDATE ON doctors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- 初始化测试数据
-- ============================================

-- 插入患者数据
INSERT INTO patients (id, name, age, gender, phone, address, medical_condition, notes) VALUES
(1, '张三', 35, '男', '13800138001', '北京市朝阳区', '感冒发烧', ''),
(2, '李四', 28, '女', '13800138002', '上海市浦东新区', '肺炎', ''),
(3, '王五', 45, '男', '13800138003', '深圳市南山区', '高血压', '定期检查血压');

-- 重置患者表序列
SELECT setval('patients_id_seq', (SELECT MAX(id) FROM patients));

-- 插入医生数据
INSERT INTO doctors (id, name, specialty, experience, phone, status, notes) VALUES
(1, '李医生', '内科', '10年', '13800138004', '在职', '主任医师'),
(2, '王医生', '外科', '8年', '13800138005', '在职', '副主任医师'),
(3, '赵医生', '儿科', '5年', '13800138006', '休息中', '主治医师');

-- 重置医生表序列
SELECT setval('doctors_id_seq', (SELECT MAX(id) FROM doctors));

-- 插入预约数据
INSERT INTO appointments (id, patient_name, doctor_name, appointment_time, status, reason, notes) VALUES
(1, '张三', '李医生', '2024-01-15 09:00:00', 'confirmed', '例行体检', NULL),
(2, '李四', '王医生', '2024-01-16 10:30:00', 'pending', '肺炎复查', NULL),
(3, '王五', '赵医生', '2024-01-17 14:00:00', 'confirmed', '血压检查', NULL);

-- 重置预约表序列
SELECT setval('appointments_id_seq', (SELECT MAX(id) FROM appointments));
```

---

## 数据字段说明

### 1. 患者表 (patients)

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | SERIAL | 是 | 主键，自增 |
| name | VARCHAR(100) | 是 | 患者姓名 |
| age | INTEGER | 是 | 年龄（0-150岁）|
| gender | VARCHAR(10) | 是 | 性别（男/女）|
| phone | VARCHAR(20) | 否 | 联系电话 |
| address | TEXT | 否 | 家庭地址 |
| medical_condition | TEXT | 是 | 病情描述 |
| notes | TEXT | 否 | 备注信息 |
| created_at | TIMESTAMP | 自动 | 创建时间 |
| updated_at | TIMESTAMP | 自动 | 更新时间 |

### 2. 医生表 (doctors)

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | SERIAL | 是 | 主键，自增 |
| name | VARCHAR(100) | 是 | 医生姓名 |
| specialty | VARCHAR(50) | 是 | 专业科室（内科/外科/儿科/妇产科/眼科/口腔科）|
| experience | VARCHAR(50) | 是 | 工作经验（如：10年）|
| phone | VARCHAR(20) | 否 | 联系电话 |
| status | VARCHAR(20) | 是 | 工作状态（在职/休息中/离职），默认：在职 |
| notes | TEXT | 否 | 备注信息（如：主任医师）|
| created_at | TIMESTAMP | 自动 | 创建时间 |
| updated_at | TIMESTAMP | 自动 | 更新时间 |

### 3. 预约表 (appointments)

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | SERIAL | 是 | 主键，自增 |
| patient_name | VARCHAR(100) | 是 | 患者姓名 |
| doctor_name | VARCHAR(100) | 是 | 医生姓名 |
| appointment_time | TIMESTAMP | 是 | 预约时间 |
| status | VARCHAR(20) | 是 | 预约状态（pending=待确认/confirmed=已确认/cancelled=已取消），默认：pending |
| reason | TEXT | 否 | 预约原因 |
| notes | TEXT | 否 | 备注信息 |
| created_at | TIMESTAMP | 自动 | 创建时间 |
| updated_at | TIMESTAMP | 自动 | 更新时间 |

---

## 索引说明

为提高查询性能，在以下字段上创建了索引：

### 患者表索引
- `idx_patients_name`: 患者姓名索引（用于按姓名搜索）
- `idx_patients_phone`: 电话号码索引（用于按电话搜索）

### 医生表索引
- `idx_doctors_name`: 医生姓名索引（用于按姓名搜索）
- `idx_doctors_specialty`: 专业科室索引（用于按科室筛选）
- `idx_doctors_status`: 工作状态索引（用于筛选在职医生）

### 预约表索引
- `idx_appointments_patient_name`: 患者姓名索引（用于查询某患者的所有预约）
- `idx_appointments_doctor_name`: 医生姓名索引（用于查询某医生的所有预约）
- `idx_appointments_time`: 预约时间索引（用于按时间范围查询）
- `idx_appointments_status`: 预约状态索引（用于筛选不同状态的预约）

---

## PostgreSQL 特色功能

### 数据完整性约束
- **CHECK 约束**: 使用CHECK约束确保年龄范围（0-150岁）和枚举值
- **触发器**: 自动更新 `updated_at` 字段
- **序列管理**: SERIAL 类型自动管理自增序列

### 中文编码支持
- **数据库字符集**: UTF8 编码
- **中文排序规则**: LC_COLLATE = 'zh_CN.UTF-8'（需要系统级中文支持）
- **注释**: 所有表和列都有中文注释方便维护

---

## 初始化测试数据包含内容

- **患者数据**: 3条示例患者记录
- **医生数据**: 3条示例医生记录（分别在职和休息中）
- **预约数据**: 3条预约记录（包含不同状态）
- **序列重置**: 确保ID从1开始

---

## 执行方法

```bash
psql -U postgres -f DATABASE_PostgreSQL_DDL.md
```

或在PostgreSQL命令行中：

```bash
psql -U postgres
\i /path/to/DATABASE_PostgreSQL_DDL.md
```

或创建数据库后：

```bash
psql -U postgres -d hospital_management -f DATABASE_PostgreSQL_DDL.md
```

---

## 注意事项

1. **序列管理**: PostgreSQL使用SERIAL和SEQUENCE管理自增主键
2. **触发器**: 需要超级用户权限创建函数
3. **字符集**: 推荐在Linux系统上使用完整的zh_CN.UTF-8本地化
