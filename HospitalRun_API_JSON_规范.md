# HospitalRun API 交互JSON规范

## 🚀 **HospitalRun API 交互JSON规范**

### **API 基础信息**
- **Base URL**: `http://localhost:3000/api`
- **字符集**: UTF-8
- **数据格式**: JSON
- **认证**: 暂无 (可后续扩展JWT)

---

## 👥 **1. 患者相关接口 (Patients)**

### **1.1 创建患者 - POST `/api/patients`**

**请求示例:**
```json
{
  "method": "POST",
  "url": "http://localhost:3000/api/patients",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "name": "张三",
    "age": 35,
    "gender": "男",
    "phone": "13800138001",
    "address": "北京市朝阳区",
    "medical_condition": "感冒发烧",
    "notes": ""
  }
}
```

**成功响应:**
```json
{
  "success": true,
  "data": {
    "id": 4,
    "name": "张三",
    "age": 35,
    "gender": "男",
    "phone": "13800138001",
    "address": "北京市朝阳区",
    "medical_condition": "感冒发烧",
    "notes": "",
    "created_at": "2024-12-10T10:30:00Z",
    "updated_at": "2024-12-10T10:30:00Z"
  },
  "message": "患者创建成功"
}
```

**错误响应:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "数据验证失败",
    "details": [
      "姓名不能为空",
      "年龄必须在0-150之间"
    ]
  }
}
```

### **1.2 获取患者列表 - GET `/api/patients`**

**查询参数:**
- `page=1` (页码)
- `limit=10` (每页数量)
- `search=张三` (姓名搜索)
- `gender=男` (性别筛选)

**请求示例:**
```json
{
  "method": "GET",
  "url": "http://localhost:3000/api/patients?page=1&limit=10&search=张三"
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "patients": [
      {
        "id": 1,
        "name": "张三",
        "age": 35,
        "gender": "男",
        "phone": "13800138001",
        "address": "北京市朝阳区",
        "medical_condition": "感冒发烧",
        "notes": "",
        "created_at": "2024-12-09T15:30:00Z",
        "updated_at": "2024-12-09T15:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 3,
      "totalPages": 1
    }
  }
}
```

### **1.3 获取单个患者 - GET `/api/patients/:id`**

**请求示例:**
```json
{
  "method": "GET",
  "url": "http://localhost:3000/api/patients/1"
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "张三",
    "age": 35,
    "gender": "男",
    "phone": "13800138001",
    "address": "北京市朝阳区",
    "medical_condition": "感冒发烧",
    "notes": "",
    "created_at": "2024-12-09T15:30:00Z",
    "updated_at": "2024-12-10T09:45:00Z"
  }
}
```

### **1.4 更新患者 - PUT `/api/patients/:id`**

**请求示例:**
```json
{
  "method": "PUT",
  "url": "http://localhost:3000/api/patients/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "name": "张三",
    "age": 36,
    "gender": "男",
    "phone": "13800138001",
    "address": "北京市海淀区",
    "medical_condition": "肺炎康复中",
    "notes": "定期随访"
  }
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "张三",
    "age": 36,
    "gender": "男",
    "phone": "13800138001",
    "address": "北京市海淀区",
    "medical_condition": "肺炎康复中",
    "notes": "定期随访",
    "created_at": "2024-12-09T15:30:00Z",
    "updated_at": "2024-12-10T09:45:00Z"
  },
  "message": "患者信息更新成功"
}
```

### **1.5 删除患者 - DELETE `/api/patients/:id`**

**请求示例:**
```json
{
  "method": "DELETE",
  "url": "http://localhost:3000/api/patients/1"
}
```

**响应示例:**
```json
{
  "success": true,
  "message": "患者删除成功"
}
```

---

## 👨‍⚕️ **2. 医生相关接口 (Doctors)**

### **2.1 创建医生 - POST `/api/doctors`**

**请求示例:**
```json
{
  "method": "POST",
  "url": "http://localhost:3000/api/doctors",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "name": "李医生",
    "specialty": "内科",
    "experience": "10年",
    "phone": "13800138004",
    "status": "在职",
    "notes": "主任医师"
  }
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "id": 4,
    "name": "李医生",
    "specialty": "内科",
    "experience": "10年",
    "phone": "13800138004",
    "status": "在职",
    "notes": "主任医师",
    "created_at": "2024-12-10T10:30:00Z",
    "updated_at": "2024-12-10T10:30:00Z"
  },
  "message": "医生创建成功"
}
```

### **2.2 获取医生列表 - GET `/api/doctors`**

**查询参数:**
- `specialty=内科` - 按专业筛选
- `status=在职` - 按状态筛选
- `search=李医生` - 姓名搜索

**响应示例 (按专业分组显示):**
```json
{
  "success": true,
  "data": {
    "doctors": [
      {
        "id": 1,
        "name": "李医生",
        "specialty": "内科",
        "experience": "10年",
        "phone": "13800138004",
        "status": "在职",
        "notes": "主任医师"
      },
      {
        "id": 2,
        "name": "王医生",
        "specialty": "外科",
        "experience": "8年",
        "phone": "13800138005",
        "status": "在职",
        "notes": "副主任医师"
      }
    ],
    "summary": {
      "total": 3,
      "specialty_count": {
        "内科": 1,
        "外科": 1,
        "儿科": 1
      },
      "status_count": {
        "在职": 2,
        "休息中": 1
      }
    }
  }
}
```

---

## 📅 **3. 预约相关接口 (Appointments)**

### **3.1 创建预约 - POST `/api/appointments`**

**请求示例:**
```json
{
  "method": "POST",
  "url": "http://localhost:3000/api/appointments",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "patient_name": "张三",
    "doctor_name": "李医生",
    "appointment_time": "2024-12-15 09:00:00",
    "status": "pending",
    "reason": "例行体检",
    "notes": ""
  }
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "id": 4,
    "patient_name": "张三",
    "doctor_name": "李医生",
    "appointment_time": "2024-12-15 09:00:00",
    "status": "pending",
    "reason": "例行体检",
    "notes": "",
    "created_at": "2024-12-10T10:30:00Z",
    "updated_at": "2024-12-10T10:30:00Z"
  },
  "message": "预约创建成功"
}
```

### **3.2 获取预约列表 - GET `/api/appointments`**

**查询参数:**
- `date_from=2024-12-01` - 开始日期
- `date_to=2024-12-31` - 结束日期
- `status=confirmed` - 预约状态
- `doctor=李医生` - 医生筛选
- `patient=张三` - 患者筛选

**响应示例 (包含患者和医生详细信息):**
```json
{
  "success": true,
  "data": {
    "appointments": [
      {
        "id": 1,
        "patient": {
          "name": "张三",
          "age": 35,
          "gender": "男",
          "phone": "13800138001",
          "condition": "感冒发烧"
        },
        "doctor": {
          "name": "李医生",
          "specialty": "内科",
          "experience": "10年"
        },
        "appointment_time": "2024-12-15 09:00:00",
        "status": "confirmed",
        "reason": "例行体检",
        "notes": "",
        "created_at": "2024-12-09T15:30:00Z",
        "updated_at": "2024-12-10T09:45:00Z"
      }
    ],
    "today_summary": {
      "total": 3,
      "confirmed": 2,
      "pending": 1,
      "cancelled": 0
    }
  }
}
```

### **3.3 更新预约 - PUT `/api/appointments/:id`**

**请求示例:**
```json
{
  "method": "PUT",
  "url": "http://localhost:3000/api/appointments/1",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "patient_name": "张三",
    "doctor_name": "李医生",
    "appointment_time": "2024-12-15 10:30:00",
    "status": "confirmed",
    "reason": "详细体检",
    "notes": "需带既往病历"
  }
}
```

**响应示例:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "patient_name": "张三",
    "doctor_name": "李医生",
    "appointment_time": "2024-12-15 10:30:00",
    "status": "confirmed",
    "reason": "详细体检",
    "notes": "需带既往病历",
    "created_at": "2024-12-09T15:30:00Z",
    "updated_at": "2024-12-10T09:45:00Z"
  },
  "message": "预约更新成功"
}
```

---

## 📊 **4. 统计与概览接口**

### **4.1 系统统计概览 - GET `/api/dashboard`**

**响应示例:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_patients": 45,
      "total_doctors": 8,
      "total_appointments_today": 12,
      "appointments_this_week": 45,
      "pending_cases": 3
    },
    "recent_appointments": [
      {
        "id": 1,
        "patient_name": "张三",
        "doctor_name": "李医生",
        "appointment_time": "2024-12-15 09:00:00",
        "status": "confirmed",
        "reason": "例行体检"
      }
    ],
    "departments": [
      {
        "name": "内科",
        "doctor_count": 2,
        "appointment_count": 15
      }
    ]
  }
}
```

---

## ⚠️ **5. 错误响应格式**

### **5.1 验证错误**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "数据验证失败",
    "details": {
      "age": "年龄必须在0-150岁之间",
      "specialty": "专业必须是有效的科室名称",
      "appointment_time": "预约时间不得早于当前时间"
    }
  }
}
```

### **5.2 资源不存在**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "资源不存在",
    "details": "患者ID为999的记录不存在"
  }
}
```

### **5.3 系统错误**
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "系统内部错误，请稍后重试",
    "details": null
  }
}
```

---

## 🔧 **6. 数据约束与业务规则**

### **6.1 前端表单验证映射**
```javascript
// 患者表单验证
const patientValidation = {
  name: { required: true, maxLength: 100 },
  age: { required: true, min: 0, max: 150 },
  gender: { required: true, enum: ['男', '女'] },
  phone: { pattern: /^1[3-9]\d{9}$/ },
  address: { maxLength: 500 },
  medical_condition: { required: true }
}

// 医生表单验证
const doctorValidation = {
  name: { required: true, maxLength: 100 },
  specialty: {
    required: true,
    enum: ['内科', '外科', '儿科', '妇产科', '眼科', '口腔科']
  },
  experience: { required: true },
  phone: { pattern: /^1[3-9]\d{9}$/ },
  status: {
    required: true,
    enum: ['在职', '休息中', '离职'],
    default: '在职'
  }
}

// 预约表单验证
const appointmentValidation = {
  patient_name: { required: true },
  doctor_name: { required: true },
  appointment_time: {
    required: true,
    future: true // 编辑时不强制要求未来
  },
  status: {
    enum: ['pending', 'confirmed', 'cancelled'],
    default: 'pending'
  }
}
```

---

## 🎯 **总结：医院管理系统API规范**

本API设计完全基于：
- ✅ **DATABASE_MySQL_DDL.md** 表结构定义
- ✅ **React组件** 实际数据需求
- ✅ **用户操作流程** 业务逻辑

**兼容特性的RESTful设计确保医院管理系统能够高效、安全、可靠地处理患者、医生和预约的全生命周期管理。** 🏥✨

---

## 📋 **版本信息**

- **规范版本**: 1.0.0
- **创建日期**: 2024-12-10
- **API版本**: v1
- **兼容性**: MySQL 5.7+ / PostgreSQL 12+
- **前端框架**: React 18+
- **文档格式**: JSON API Specification

---

*本规范为HospitalRun医院管理系统的标准API接口定义，确保前后端开发的统一性和规范性。*
