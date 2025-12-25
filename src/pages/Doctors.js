import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Fab,
  Chip,
  Alert,
  Snackbar,
  CircularProgress,
  Box,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import DoctorForm from '../components/DoctorForm';
import { useLanguage } from '../contexts/LanguageContext';
import { doctorAPI } from '../services/api';

const Doctors = () => {
  const { t } = useLanguage();
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formOpen, setFormOpen] = useState(false);
  const [editingDoctor, setEditingDoctor] = useState(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success',
  });

  // 加载医生数据
  const loadDoctors = async () => {
    try {
      setLoading(true);
      const response = await doctorAPI.getDoctors();
      if (response.success && response.data.doctors) {
        setDoctors(response.data.doctors);
      }
    } catch (error) {
      console.error('Failed to load doctors:', error);
      setSnackbar({
        open: true,
        message: '加载医生数据失败',
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDoctors();
  }, []);

  const handleAddDoctor = () => {
    setEditingDoctor(null);
    setFormOpen(true);
  };

  const handleEditDoctor = (doctor) => {
    setEditingDoctor(doctor);
    setFormOpen(true);
  };

  const handleSaveDoctor = async (formData) => {
    try {
      let response;
      if (editingDoctor) {
        // 更新医生
        response = await doctorAPI.updateDoctor(editingDoctor.id, formData);
        if (response.success) {
          setSnackbar({
            open: true,
            message: '医生信息更新成功',
            severity: 'success',
          });
        }
      } else {
        // 创建医生
        response = await doctorAPI.createDoctor(formData);
        if (response.success) {
          setSnackbar({
            open: true,
            message: '医生创建成功',
            severity: 'success',
          });
        }
      }
      // 重新加载医生列表
      await loadDoctors();
      setFormOpen(false);
    } catch (error) {
      console.error('Failed to save doctor:', error);
      setSnackbar({
        open: true,
        message: editingDoctor ? '更新医生失败' : '创建医生失败',
        severity: 'error',
      });
    }
  };

  const handleDeleteDoctor = async (doctor) => {
    if (!window.confirm(`确定要删除医生 ${doctor.name} 吗？`)) {
      return;
    }

    try {
      const response = await doctorAPI.deleteDoctor(doctor.id);
      if (response.success) {
        setSnackbar({
          open: true,
          message: '医生删除成功',
          severity: 'success',
        });
        // 重新加载医生列表
        await loadDoctors();
      }
    } catch (error) {
      console.error('Failed to delete doctor:', error);
      setSnackbar({
        open: true,
        message: '删除医生失败',
        severity: 'error',
      });
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case '在职': return t('statusOnDuty');
      case '休息中': return t('statusOnLeave');
      case '离职': return t('statusResigned');
      default: return status;
    }
  };

  const getSpecialtyText = (specialty) => {
    switch (specialty) {
      case '内科': return t('internalMedicine');
      case '外科': return t('surgery');
      case '儿科': return t('pediatrics');
      case '妇产科': return t('gynecology');
      case '眼科': return t('ophthalmology');
      case '口腔科': return t('dentistry');
      default: return specialty;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case '在职':
        return 'success';
      case '休息中':
        return 'warning';
      case '离职':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom component="div">
        <ManageAccountsIcon sx={{ mr: 1 }} />
        {t('doctors')}
      </Typography>

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label={t('doctorList')}>
          <TableHead>
            <TableRow>
              <TableCell>{t('name')}</TableCell>
              <TableCell>{t('specialty')}</TableCell>
              <TableCell>{t('experience')}</TableCell>
              <TableCell>{t('phone')}</TableCell>
              <TableCell>{t('status')}</TableCell>
              <TableCell sx={{ pl: 8 }}>{t('edit')}</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={6} align="center">
                  <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                    <CircularProgress />
                    <Typography sx={{ ml: 2 }}>加载中...</Typography>
                  </Box>
                </TableCell>
              </TableRow>
            ) : doctors.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ py: 4 }}>
                  <Typography variant="body1" color="text.secondary">
                    暂无医生数据
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              doctors.map((doctor) => (
                <TableRow key={doctor.id}>
                  <TableCell>{doctor.name}</TableCell>
                  <TableCell>{getSpecialtyText(doctor.specialty)}</TableCell>
                  <TableCell>{doctor.experience}</TableCell>
                  <TableCell>{doctor.phone || '-'}</TableCell>
                  <TableCell>
                    <Chip
                      label={getStatusText(doctor.status)}
                      color={getStatusColor(doctor.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Button
                      size="small"
                      color="primary"
                      onClick={() => handleEditDoctor(doctor)}
                    >
                      <EditIcon fontSize="small" />
                    </Button>
                    <Button
                      size="small"
                      color="error"
                      onClick={() => handleDeleteDoctor(doctor)}
                    >
                      <DeleteIcon fontSize="small" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <DoctorForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSave={handleSaveDoctor}
        doctor={editingDoctor}
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
        onClick={handleAddDoctor}
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

export default Doctors;
