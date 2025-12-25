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
import { useLanguage } from '../contexts/LanguageContext';

const DoctorForm = ({ open, onClose, onSave, doctor = null }) => {
  const { t } = useLanguage();
  const [formData, setFormData] = useState({
    name: '',
    specialty: '',
    experience: '',
    phone: '',
    status: '在职',
    notes: '',
  });

  useEffect(() => {
    if (doctor) {
      setFormData({
        name: doctor.name || '',
        specialty: doctor.specialty || '',
        experience: doctor.experience || '',
        phone: doctor.phone || '',
        status: doctor.status || '',
        notes: doctor.notes || '',
      });
    } else {
      setFormData({
        name: '',
        specialty: '',
        experience: '',
        phone: '',
        status: '在职',
        notes: '',
      });
    }
  }, [doctor, open]);

  const handleChange = (field) => (event) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };

  const handleSubmit = () => {
    if (!formData.name || !formData.specialty || !formData.experience) {
      alert(t('requiredFieldsError', '请填写医生姓名、专业和经验等必填字段'));
      return;
    }

    onSave(formData);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {doctor ? t('editDoctor') : t('addDoctor')}
      </DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 1 }}>
          <TextField
            margin="dense"
            label={t('doctorName', '医生姓名')}
            fullWidth
            variant="outlined"
            value={formData.name}
            onChange={handleChange('name')}
            required
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>{t('specialty')}</InputLabel>
            <Select
              value={formData.specialty}
              label={t('specialty')}
              onChange={handleChange('specialty')}
            >
              <MenuItem value="内科">{t('internalMedicine', '内科')}</MenuItem>
              <MenuItem value="外科">{t('surgery', '外科')}</MenuItem>
              <MenuItem value="儿科">{t('pediatrics', '儿科')}</MenuItem>
              <MenuItem value="妇产科">{t('gynecology', '妇产科')}</MenuItem>
              <MenuItem value="眼科">{t('ophthalmology', '眼科')}</MenuItem>
              <MenuItem value="口腔科">{t('dentistry', '口腔科')}</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            label={t('experience')}
            fullWidth
            variant="outlined"
            placeholder={t('experiencePlaceholder', '例如：10年')}
            value={formData.experience}
            onChange={handleChange('experience')}
            required
          />
          <TextField
            margin="dense"
            label={t('phone')}
            fullWidth
            variant="outlined"
            value={formData.phone}
            onChange={handleChange('phone')}
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>{t('status')}</InputLabel>
            <Select
              value={formData.status}
              label={t('status')}
              onChange={handleChange('status')}
            >
              <MenuItem value="在职">{t('statusOnDuty')}</MenuItem>
              <MenuItem value="休息中">{t('statusOnLeave')}</MenuItem>
              <MenuItem value="离职">{t('statusResigned')}</MenuItem>
            </Select>
          </FormControl>
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
          {doctor ? t('save') : t('add')}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DoctorForm;
