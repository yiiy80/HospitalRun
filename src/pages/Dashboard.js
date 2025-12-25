import React, { useState, useEffect } from 'react';
import { Container, Grid, Paper, Typography, Box, Alert, Snackbar, CircularProgress } from '@mui/material';
import { styled } from '@mui/material/styles';
import { useLanguage } from '../contexts/LanguageContext';
import DashboardIcon from '@mui/icons-material/Dashboard';
import { dashboardAPI } from '../services/api';

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  padding: theme.spacing(2),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

const Dashboard = () => {
  const { t } = useLanguage();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success',
  });

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const response = await dashboardAPI.getDashboard();
      if (response.success && response.data) {
        setDashboardData(response.data);
      }
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      setSnackbar({
        open: true,
        message: '加载仪表盘数据失败',
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const stats = dashboardData ? [
    { titleKey: 'totalPatients', value: dashboardData.summary.total_patients },
    { titleKey: 'todayAppointments', value: dashboardData.summary.total_appointments_today },
    { titleKey: 'pendingCases', value: dashboardData.summary.pending_cases },
    { titleKey: 'departments', value: dashboardData.departments.length },
  ] : [
    { titleKey: 'totalPatients', value: 0 },
    { titleKey: 'todayAppointments', value: 0 },
    { titleKey: 'pendingCases', value: 0 },
    { titleKey: 'departments', value: 0 },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        <DashboardIcon sx={{ mr: 1 }} />
        {t('title')}
      </Typography>
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 200 }}>
          <CircularProgress />
          <Typography sx={{ ml: 2 }}>加载仪表盘数据...</Typography>
        </Box>
      ) : (
        <Grid container spacing={3}>
          {stats.map((stat, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Item>
                <Typography variant="h5">{stat.value}</Typography>
                <Typography variant="subtitle1">{t(stat.titleKey)}</Typography>
              </Item>
            </Grid>
          ))}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                近期预约
              </Typography>
              {dashboardData?.recent_appointments && dashboardData.recent_appointments.length > 0 ? (
                <Box sx={{ maxHeight: 300, overflowY: 'auto' }}>
                  {dashboardData.recent_appointments.map((appointment, index) => (
                    <Box key={index} sx={{ mb: 2, pb: 2, borderBottom: '1px solid #f0f0f0' }}>
                      <Typography variant="subtitle1" fontWeight="bold">
                        {appointment.patient_name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        医生: {appointment.doctor_name} | 时间: {formatDate(appointment.appointment_time)}
                      </Typography>
                      <Typography variant="body2">
                        状态: {appointment.status === 'confirmed' ? '已确认' : appointment.status === 'pending' ? '待确认' : '已取消'}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
                  暂无近期预约
                </Typography>
              )}
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                科室统计
              </Typography>
              {dashboardData?.departments && dashboardData.departments.length > 0 ? (
                <Box>
                  {dashboardData.departments.map((dept, index) => (
                    <Box key={index} sx={{ mb: 1 }}>
                      <Typography variant="body2">
                        {dept.name}: {dept.doctor_count}名医生, {dept.appointment_count}个预约
                      </Typography>
                    </Box>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
                  暂无科室数据
                </Typography>
              )}
            </Paper>
          </Grid>
        </Grid>
      )}

      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Container>
  );
};

export default Dashboard;
