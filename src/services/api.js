// HospitalRun API 服务
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// 通用API请求函数
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  console.log('API Request:', options.method || 'GET', url);

  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    console.log('API Response Status:', response.status, response.statusText);

    // 处理不同类型的响应
    if (response.status === 204) {
      // No Content
      console.log('API Response: No Content');
      return { success: true, data: null };
    }

    let data;
    const contentType = response.headers.get('content-type');
    console.log('Response Content-Type:', contentType);

    if (contentType && contentType.includes('application/json')) {
      data = await response.json();
      console.log('API Response Data:', data);
    } else {
      data = await response.text();
      console.log('API Response Text:', data);
    }

    if (!response.ok) {
      // 服务器返回错误状态
      if (data && data.success === false && data.error) {
        console.error('API Error:', data.error);
        throw new Error(data.error.message || 'API request failed');
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
    }

  // 对于dashboard端点，直接返回数据（FastAPI后端没有wrapped格式）
  if (endpoint === '/dashboard') {
    console.log('Dashboard API Response:', data);
    return { success: true, data: data };
  }

  return data;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

// ============================================
// 患者相关API
// ============================================

export const patientAPI = {
  // 获取患者列表 (支持分页、搜索、筛选)
  getPatients: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/patients?${queryString}` : '/patients';

    // 列表端点直接返回数据
    const url = `${API_BASE_URL}${endpoint}`;
    console.log('API Request: GET', url);

    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('API Response Status:', response.status, response.statusText);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('API Response Data:', data);

      // 列表端点直接返回数据，不是wrapped格式
      return {
        success: true,
        data: data  // 直接返回 PatientListResponse
      };
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  },

  // 获取单个患者
  getPatient: (id) => apiRequest(`/patients/${id}`),

  // 创建患者
  createPatient: (data) => apiRequest('/patients', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  // 更新患者
  updatePatient: (id, data) => apiRequest(`/patients/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),

  // 删除患者
  deletePatient: (id) => apiRequest(`/patients/${id}`, {
    method: 'DELETE',
  }),
};

// ============================================
// 医生相关API
// ============================================

export const doctorAPI = {
  // 获取医生列表 (支持筛选)
  getDoctors: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/doctors?${queryString}` : '/doctors';

    // 列表端点直接返回数据
    const url = `${API_BASE_URL}${endpoint}`;
    console.log('API Request: GET', url);

    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('API Response Status:', response.status, response.statusText);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('API Response Data:', data);

      // 列表端点直接返回数据，不是wrapped格式
      return {
        success: true,
        data: data  // 直接返回 DoctorListResponse
      };
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  },

  // 获取单个医生
  getDoctor: (id) => apiRequest(`/doctors/${id}`),

  // 创建医生
  createDoctor: (data) => apiRequest('/doctors', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  // 更新医生
  updateDoctor: (id, data) => apiRequest(`/doctors/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),

  // 删除医生
  deleteDoctor: (id) => apiRequest(`/doctors/${id}`, {
    method: 'DELETE',
  }),
};

// ============================================
// 预约相关API
// ============================================

export const appointmentAPI = {
  // 获取预约列表 (支持筛选)
  getAppointments: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = queryString ? `/appointments?${queryString}` : '/appointments';

    // 列表端点直接返回数据
    const url = `${API_BASE_URL}${endpoint}`;
    console.log('API Request: GET', url);

    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('API Response Status:', response.status, response.statusText);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('API Response Data:', data);

      // 列表端点直接返回数据，不是wrapped格式
      return {
        success: true,
        data: data  // 直接返回 AppointmentListResponse
      };
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  },

  // 获取单个预约
  getAppointment: (id) => apiRequest(`/appointments/${id}`),

  // 创建预约
  createAppointment: (data) => apiRequest('/appointments', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  // 更新预约
  updateAppointment: (id, data) => apiRequest(`/appointments/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),

  // 删除预约
  deleteAppointment: (id) => apiRequest(`/appointments/${id}`, {
    method: 'DELETE',
  }),
};

// ============================================
// 仪表盘相关API
// ============================================

export const dashboardAPI = {
  // 获取仪表盘统计数据
  getDashboard: () => apiRequest('/dashboard'),
};

// ============================================
// 健康检查
// ============================================

export const healthAPI = {
  check: () => fetch(`${API_BASE_URL.replace('/api', '')}/health`).then(res => res.json()),
};

// 默认导出API对象
const api = {
  patients: patientAPI,
  doctors: doctorAPI,
  appointments: appointmentAPI,
  dashboard: dashboardAPI,
  health: healthAPI,
};

export default api;
