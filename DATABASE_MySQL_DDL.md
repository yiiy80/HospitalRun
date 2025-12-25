# 医院管理系统 - MySQL DDL

## 数据模型概览

本系统包含三个核心实体：
- **患者 (Patients)** - 管理患者基本信息和病情
- **医生 (Doctors)** - 管理医生信息、专业和状态
- **预约 (Appointments)** - 管理患者与医生的预约记录

---

## MySQL DDL

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS hospital_management
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE hospital_management;

-- ============================================
-- 1. 患者表 (Patients)
-- ============================================
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '患者ID',
    name VARCHAR(100) NOT NULL COMMENT '患者姓名',
    age INT NOT NULL COMMENT '年龄',
    gender ENUM('男', '女') NOT NULL COMMENT '性别',
    phone VARCHAR(20) COMMENT '联系电话',
    address TEXT COMMENT '家庭地址',
    medical_condition TEXT NOT NULL COMMENT '病情描述',
    notes TEXT COMMENT '备注信息',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (name),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='患者信息表';

-- ============================================
-- 2. 医生表 (Doctors)
-- ============================================
CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '医生ID',
    name VARCHAR(100) NOT NULL COMMENT '医生姓名',
    specialty ENUM('内科', '外科', '儿科', '妇产科', '眼科', '口腔科') NOT NULL COMMENT '专业科室',
    experience VARCHAR(50) NOT NULL COMMENT '工作经验（如：10年）',
    phone VARCHAR(20) COMMENT '联系电话',
    status ENUM('在职', '休息中', '离职') NOT NULL DEFAULT '在职' COMMENT '工作状态',
    notes TEXT COMMENT '备注信息（如：主任医师）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_name (name),
    INDEX idx_specialty (specialty),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='医生信息表';

-- ============================================
-- 3. 预约表 (Appointments)
-- ============================================
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '预约ID',
    patient_name VARCHAR(100) NOT NULL COMMENT '患者姓名',
    doctor_name VARCHAR(100) NOT NULL COMMENT '医生姓名',
    appointment_time DATETIME NOT NULL COMMENT '预约时间',
    status ENUM('pending', 'confirmed', 'cancelled') NOT NULL DEFAULT 'pending' COMMENT '预约状态：待确认/已确认/已取消',
    reason TEXT COMMENT '预约原因',
    notes TEXT COMMENT '备注信息',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_patient_name (patient_name),
    INDEX idx_doctor_name (doctor_name),
    INDEX idx_appointment_time (appointment_time),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='预约记录表';

-- ============================================
-- 初始化测试数据
-- ============================================

-- 插入患者数据
INSERT INTO patients (id, name, age, gender, phone, address, medical_condition, notes) VALUES
(1, '张三', 35, '男', '13800138001', '北京市朝阳区', '感冒发烧', ''),
(2, '李四', 28, '女', '13800138002', '上海市浦东新区', '肺炎', ''),
(3, '王五', 45, '男', '13800138003', '深圳市南山区', '高血压', '定期检查血压');

-- 插入医生数据
INSERT INTO doctors (id, name, specialty, experience, phone, status, notes) VALUES
(1, '李医生', '内科', '10年', '13800138004', '在职', '主任医师'),
(2, '王医生', '外科', '8年', '13800138005', '在职', '副主任医师'),
(3, '赵医生', '儿科', '5年', '13800138006', '休息中', '主治医师');

-- 插入预约数据
INSERT INTO appointments (id, patient_name, doctor_name, appointment_time, status, reason, notes) VALUES
(1, '张三', '李医生', '2024-01-15 09:00:00', 'confirmed', '例行体检', NULL),
(2, '李四', '王医生', '2024-01-16 10:30:00', 'pending', '肺炎复查', NULL),
(3, '王五', '赵医生', '2024-01-17 14:00:00', 'confirmed', '血压检查', NULL);
```

---

## 数据字段说明

### 1. 患者表 (patients)

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | INT/SERIAL | 是 | 主键，自增 |
| name | VARCHAR(100) | 是 | 患者姓名 |
| age | INT | 是 | 年龄 |
| gender | ENUM/VARCHAR | 是 | 性别（男/女）|
| phone | VARCHAR(20) | 否 | 联系电话 |
| address | TEXT | 否 | 家庭地址 |
| medical_condition | TEXT | 是 | 病情描述 |
| notes | TEXT | 否 | 备注信息 |
| created_at | TIMESTAMP | 自动 | 创建时间 |
| updated_at | TIMESTAMP | 自动 | 更新时间 |

### 2. 医生表 (doctors)

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | INT/SERIAL | 是 | 主键，自增 |
| name | VARCHAR(100) | 是 | 医生姓名 |
| specialty | ENUM/VARCHAR | 是 | 专业科室（内科/外科/儿科/妇产科/眼科/口腔科）|
| experience | VARCHAR(50) | 是 | 工作经验（如：10年）|
| phone | VARCHAR(20) | 否 | 联系电话 |
| status | ENUM/VARCHAR | 是 | 工作状态（在职/休息中/离职），默认：在职 |
| notes | TEXT | 否 | 备注信息（如：主任医师）|
| created_at | TIMESTAMP | 自动 | 创建时间 |
| updated_at | TIMESTAMP | 自动 | 更新时间 |

### 3. 预约表 (appointments)

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | INT/SERIAL | 是 | 主键，自增 |
| patient_name | VARCHAR(100) | 是 | 患者姓名 |
| doctor_name | VARCHAR(100) | 是 | 医生姓名 |
| appointment_time | DATETIME/TIMESTAMP | 是 | 预约时间 |
| status | ENUM/VARCHAR | 是 | 预约状态（pending=待确认/confirmed=已确认/cancelled=已取消），默认：pending |
| reason | TEXT | 否 | 预约原因 |
| notes | TEXT | 否 | 备注信息 |
| created_at | TIMESTAMP | 自动 | 创建时间 |
| updated_at | TIMESTAMP | 自动 | 更新时间 |

---

## 索引说明

为提高查询性能，在以下字段上创建了索引：

### 患者表索引
- `idx_name`: 患者姓名索引（用于按姓名搜索）
- `idx_phone`: 电话号码索引（用于按电话搜索）

### 医生表索引
- `idx_name`: 医生姓名索引（用于按姓名搜索）
- `idx_specialty`: 专业科室索引（用于按科室筛选）
- `idx_status`: 工作状态索引（用于筛选在职医生）

### 预约表索引
- `idx_patient_name`: 患者姓名索引（用于查询某患者的所有预约）
- `idx_doctor_name`: 医生姓名索引（用于查询某医生的所有预约）
- `idx_appointment_time`: 预约时间索引（用于按时间范围查询）
- `idx_status`: 预约状态索引（用于筛选不同状态的预约）

---

## 初始化测试数据包含内容

- **患者数据**: 3条示例患者记录
- **医生数据**: 3条示例医生记录（分别在职和休息中）
- **预约数据**: 3条预约记录（包含不同状态）

---

## 执行方法

```bash
mysql -u root -p < DATABASE_MySQL_DDL.md
```

或

```bash
mysql -u root -p
source /path/to/DATABASE_MySQL_DDL.md
