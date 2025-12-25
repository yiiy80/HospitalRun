import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  List,
  ListItem,
  ListItemText,
  Paper,
  Chip,
  Fab,
  Button,
  Alert,
  Snackbar,
  CircularProgress,
  Box,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AppointmentForm from '../components/AppointmentForm';
import EventNoteIcon from '@mui/icons-material/EventNote';
import { useLanguage } from '../contexts/LanguageContext';
import { appointmentAPI, patientAPI, doctorAPI } from '../services/api';

const Appointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formOpen, setFormOpen] = useState(false);
  const [editingAppointment, setEditingAppointment] = useState(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success',
  });

  const handleAddAppointment = () => {
    setEditingAppointment(null);
    setFormOpen(true);
  };

  const handleEditAppointment = (appointment) => {
    setEditingAppointment(appointment);
    setFormOpen(true);
  };

  // 加载数据
  const loadData = async () => {
    try {
      setLoading(true);
      const appointmentsRes = await appointmentAPI.getAppointments();

      if (appointmentsRes.success && appointmentsRes.data.appointments) {
        setAppointments(appointmentsRes.data.appointments);
      }
    } catch (error) {
      console.error('Failed to load data:', error);
      setSnackbar({
        open: true,
        message: '加载数据失败',
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSaveAppointment = async (formData) => {
    try {
      let response;
      if (editingAppointment) {
        // 更新预约
        const updateData = {
          patient_name: formData.patient_name || formData.patient,
          doctor_name: formData.doctor_name || formData.doctor,
          appointment_time: formData.appointment_time || formData.time,
          status: formData.status,
          reason: formData.reason,
          notes: formData.notes,
        };
        response = await appointmentAPI.updateAppointment(editingAppointment.id, updateData);
        if (response.success) {
          setSnackbar({
            open: true,
            message: '预约更新成功',
            severity: 'success',
          });
        }
      } else {
        // 创建预约
        const createData = {
          patient_name: formData.patient_name || formData.patient,
          doctor_name: formData.doctor_name || formData.doctor,
          appointment_time: formData.appointment_time || formData.time,
          status: formData.status || 'pending',
          reason: formData.reason,
          notes: formData.notes,
        };
        response = await appointmentAPI.createAppointment(createData);
        if (response.success) {
          setSnackbar({
            open: true,
            message: '预约创建成功',
            severity: 'success',
          });
        }
      }
      // 重新加载预约列表
      await loadData();
      setFormOpen(false);
    } catch (error) {
      console.error('Failed to save appointment:', error);
      setSnackbar({
        open: true,
        message: editingAppointment ? '更新预约失败' : '创建预约失败',
        severity: 'error',
      });
    }
  };

  const handleDeleteAppointment = async (appointment) => {
    if (!window.confirm(`确定要删除 ${appointment.patient_name || appointment.patient} 的预约吗？`)) {
      return;
    }

    try {
      const response = await appointmentAPI.deleteAppointment(appointment.id);
      if (response.success) {
        setSnackbar({
          open: true,
          message: '预约删除成功',
          severity: 'success',
        });
        // 重新加载预约列表
        await loadData();
      }
    } catch (error) {
      console.error('Failed to delete appointment:', error);
      setSnackbar({
        open: true,
        message: '删除预约失败',
        severity: 'error',
      });
    }
  };

  const { t } = useLanguage();

  const formatDateTime = (dateTimeString) => {
    return new Date(dateTimeString).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed':
        return 'success';
      case 'pending':
        return 'warning';
      case 'cancelled':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'confirmed': return '已确认';
      case 'pending': return '待确认';
      case 'cancelled': return '已取消';
      default: return status;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        <EventNoteIcon sx={{ mr: 1 }} />
        {t('appointments')}
      </Typography>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 200 }}>
          <CircularProgress />
          <Typography sx={{ ml: 2 }}>加载预约数据...</Typography>
        </Box>
      ) : (
        <Paper sx={{ p: 2 }}>
          <List>
            {appointments.length === 0 ? (
              <ListItem>
                <ListItemText
                  primary="暂无预约数据"
                  sx={{ textAlign: 'center', py: 4 }}
                />
              </ListItem>
            ) : (
              appointments.map((appointment) => (
                <ListItem key={appointment.id} divider>
                  <ListItemText
                    primary={
                      `${appointment.patient_name || appointment.patient?.name || '未知患者'} - 
                       ${appointment.doctor_name || appointment.doctor?.name || '未知医生'}`
                    }
                    secondary={`时间: ${formatDateTime(appointment.appointment_time || appointment.time)} | 
                              原因: ${appointment.reason || '无'} | 
                              ${appointment.patient?.condition ? `病情: ${appointment.patient.condition}` : ''}`}
                  />
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Chip
                      label={getStatusText(appointment.status)}
                      color={getStatusColor(appointment.status)}
                      size="small"
                    />
                    <Button
                      size="small"
                      color="primary"
                      onClick={() => handleEditAppointment(appointment)}
                      sx={{ mr: 1 }}
                    >
                      <EditIcon fontSize="small" />
                    </Button>
                    <Button
                      size="small"
                      color="error"
                      onClick={() => handleDeleteAppointment(appointment)}
                    >
                      <DeleteIcon fontSize="small" />
                    </Button>
                  </div>
                </ListItem>
              ))
            )}
          </List>
        </Paper>
      )}

      <AppointmentForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSave={handleSaveAppointment}
        appointment={editingAppointment}
      />

      <Fab
        color="primary"
        aria-label="add"
        sx={{
          position: 'fixed',
          bottom: 16,
          right: 16,
          zIndex: 1000,
          backgroundColor: '#1976d2'
        }}
        onClick={handleAddAppointment}
      >
        <AddIcon />
      </Fab>

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

export default Appointments;
