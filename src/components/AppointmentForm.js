import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
} from '@mui/material';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { zhCN } from 'date-fns/locale';
import { useLanguage } from '../contexts/LanguageContext';
import { patientAPI, doctorAPI } from '../services/api';

const AppointmentForm = ({ open, onClose, onSave, appointment = null }) => {
  const { t } = useLanguage();
  const [formData, setFormData] = useState({
    patient: '',
    doctor: '',
    date: null,
    time: '',
    reason: '',
    notes: '',
  });
  const [patients, setPatients] = useState([]);
  const [doctors, setDoctors] = useState([]);

  // 加载患者和医生数据
  useEffect(() => {
    const loadOptions = async () => {
      try {
        const [patientsRes, doctorsRes] = await Promise.all([
          patientAPI.getPatients(),
          doctorAPI.getDoctors(),
        ]);

        if (patientsRes.success && patientsRes.data.patients) {
          setPatients(patientsRes.data.patients);
        }
        if (doctorsRes.success && doctorsRes.data.doctors) {
          setDoctors(doctorsRes.data.doctors);
        }
      } catch (error) {
        console.error('Failed to load options:', error);
      }
    };

    if (open) {
      loadOptions();
    }
  }, [open]);

  useEffect(() => {
    if (appointment) {
      const dateTimeStr = appointment.appointment_time || appointment.time;
      let dateObj = null;
      let timeStr = '';

      if (dateTimeStr) {
        const dateTime = new Date(dateTimeStr);
        dateObj = dateTime;
        timeStr = dateTime.toTimeString().substring(0, 5); // 格式化为 HH:MM
      }

      setFormData({
        patient: appointment.patient_name || appointment.patient || '',
        doctor: appointment.doctor_name || appointment.doctor || '',
        date: dateObj,
        time: timeStr,
        reason: appointment.reason || '',
        notes: appointment.notes || '',
      });
    } else {
      setFormData({
        patient: '',
        doctor: '',
        date: null,
        time: '',
        reason: '',
        notes: '',
      });
    }
  }, [appointment, open]);

  const handleChange = (field) => (event) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };

  const handleDateChange = (date) => {
    setFormData({
      ...formData,
      date: date,
    });
  };

  const handleSubmit = () => {
    if (!formData.patient || !formData.doctor || !formData.date || !formData.time) {
      alert(t('requiredFieldsError', '请填写患者姓名、医生、日期和时间等必填字段'));
      return;
    }

    // 只对新建预约验证日期是否是未来日期或今天，编辑时跳过这个检查
    if (!appointment) { // 如果是新建预约
      const today = new Date();
      today.setHours(0, 0, 0, 0); // 重置时间到今天开始

      const selectedDate = new Date(formData.date);
      selectedDate.setHours(0, 0, 0, 0); // 重置时间

      if (selectedDate < today) {
        alert(t('pastDateError', '预约日期不得早于今天，请选择未来日期'));
        return;
      }
    }

    const dateStr = formData.date.toISOString().split('T')[0];
    const fullAppointment = {
      ...formData,
      time: `${dateStr} ${formData.time}`,
      status: appointment ? appointment.status : 'pending',
    };
    onSave(fullAppointment);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {appointment ? t('editAppointment') : t('addAppointment')}
      </DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 1 }}>
          <TextField
            margin="dense"
            label={t('patientName', '患者姓名')}
            fullWidth
            variant="outlined"
            value={formData.patient}
            onChange={handleChange('patient')}
            required
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>{t('doctor')}</InputLabel>
            <Select
              value={formData.doctor}
              label={t('doctor')}
              onChange={handleChange('doctor')}
              required
            >
              {doctors.length === 0 ? (
                <MenuItem disabled>暂无医生数据</MenuItem>
              ) : (
                doctors.map((doctor) => (
                  <MenuItem key={doctor.id} value={doctor.name}>
                    {doctor.name} ({doctor.specialty})
                  </MenuItem>
                ))
              )}
            </Select>
          </FormControl>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={zhCN}>
            <DatePicker
              label={t('appointmentDate', '预约日期')}
              value={formData.date}
              onChange={handleDateChange}
              slotProps={{
                textField: {
                  fullWidth: true,
                  margin: 'dense',
                  required: true,
                }
              }}
              minDate={appointment ? undefined : new Date()}
            />
          </LocalizationProvider>
          <TextField
            margin="dense"
            label={t('appointmentTime', '预约时间')}
            fullWidth
            variant="outlined"
            type="text"
            placeholder={t('timeExample', '例如：14:30')}
            value={formData.time}
            onChange={handleChange('time')}
            required
          />
          <TextField
            margin="dense"
            label={t('reason')}
            fullWidth
            variant="outlined"
            multiline
            rows={2}
            value={formData.reason}
            onChange={handleChange('reason')}
          />
          <TextField
            margin="dense"
            label={t('notes')}
            fullWidth
            variant="outlined"
            multiline
            rows={2}
            value={formData.notes}
            onChange={handleChange('notes')}
          />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>{t('cancel')}</Button>
        <Button onClick={handleSubmit} variant="contained">
          {appointment ? t('save') : t('add')}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default AppointmentForm;
