import React, { useState, useEffect } from 'react';
import PeopleIcon from '@mui/icons-material/People';
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
  Alert,
  Snackbar,
  CircularProgress,
  Box,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import PatientForm from '../components/PatientForm';
import { useLanguage } from '../contexts/LanguageContext';
import { patientAPI } from '../services/api';

const Patients = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formOpen, setFormOpen] = useState(false);
  const [editingPatient, setEditingPatient] = useState(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success',
  });

  const { t } = useLanguage();

  // 加载患者数据
  const loadPatients = async () => {
    try {
      setLoading(true);
      const response = await patientAPI.getPatients();
      if (response.success && response.data.patients) {
        setPatients(response.data.patients);
      }
    } catch (error) {
      console.error('Failed to load patients:', error);
      setSnackbar({
        open: true,
        message: '加载患者数据失败',
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPatients();
  }, []);

  const handleAddPatient = () => {
    setEditingPatient(null);
    setFormOpen(true);
  };

  const handleEditPatient = (patient) => {
    setEditingPatient(patient);
    setFormOpen(true);
  };

  const handleSavePatient = async (formData) => {
    try {
      let response;
      if (editingPatient) {
        // 更新患者
        response = await patientAPI.updatePatient(editingPatient.id, {
          ...formData,
          medical_condition: formData.condition, // 映射字段名
        });
        if (response.success) {
          setSnackbar({
            open: true,
            message: '患者信息更新成功',
            severity: 'success',
          });
        }
      } else {
        // 创建患者
        response = await patientAPI.createPatient({
          ...formData,
          medical_condition: formData.condition, // 映射字段名
        });
        if (response.success) {
          setSnackbar({
            open: true,
            message: '患者创建成功',
            severity: 'success',
          });
        }
      }
      // 重新加载患者列表
      await loadPatients();
      setFormOpen(false);
    } catch (error) {
      console.error('Failed to save patient:', error);
      setSnackbar({
        open: true,
        message: editingPatient ? '更新患者失败' : '创建患者失败',
        severity: 'error',
      });
    }
  };

  const handleDeletePatient = async (patient) => {
    if (!window.confirm(`确定要删除患者 ${patient.name} 吗？`)) {
      return;
    }

    try {
      const response = await patientAPI.deletePatient(patient.id);
      if (response.success) {
        setSnackbar({
          open: true,
          message: '患者删除成功',
          severity: 'success',
        });
        // 重新加载患者列表
        await loadPatients();
      }
    } catch (error) {
      console.error('Failed to delete patient:', error);
      setSnackbar({
        open: true,
        message: '删除患者失败',
        severity: 'error',
      });
    }
  };

  const getGenderText = (gender) => {
    switch (gender) {
      case '男': return t('male');
      case '女': return t('female');
      default: return gender;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        <PeopleIcon sx={{ mr: 1 }} />
        {t('patients')}
      </Typography>

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label={t('patientList')}>
          <TableHead>
            <TableRow>
              <TableCell>{t('name')}</TableCell>
              <TableCell>{t('age')}</TableCell>
              <TableCell>{t('gender')}</TableCell>
              <TableCell>{t('phone')}</TableCell>
              <TableCell>{t('condition')}</TableCell>
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
            ) : patients.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} align="center" sx={{ py: 4 }}>
                  <Typography variant="body1" color="text.secondary">
                    暂无患者数据
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              patients.map((patient) => (
                <TableRow key={patient.id}>
                  <TableCell>{patient.name}</TableCell>
                  <TableCell>{patient.age}</TableCell>
                  <TableCell>{getGenderText(patient.gender)}</TableCell>
                  <TableCell>{patient.phone || '-'}</TableCell>
                  <TableCell>{patient.medical_condition || patient.condition}</TableCell>
                  <TableCell>
                    <Button
                      size="small"
                      color="primary"
                      onClick={() => handleEditPatient(patient)}
                    >
                      <EditIcon fontSize="small" />
                    </Button>
                    <Button
                      size="small"
                      color="error"
                      onClick={() => handleDeletePatient(patient)}
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

      <PatientForm
        open={formOpen}
        onClose={() => setFormOpen(false)}
        onSave={handleSavePatient}
        patient={editingPatient}
      />

      <Fab color="primary" aria-label="add" sx={{ position: 'fixed', bottom: 16, right: 16 }} onClick={handleAddPatient}>
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

export default Patients;
