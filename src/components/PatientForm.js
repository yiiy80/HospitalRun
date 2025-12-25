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

const PatientForm = ({ open, onClose, onSave, patient = null }) => {
  const { t } = useLanguage();
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    gender: '',
    phone: '',
    address: '',
    condition: '',
    notes: '',
  });

  useEffect(() => {
    if (patient) {
      setFormData({
        name: patient.name || '',
        age: patient.age || '',
        gender: patient.gender || '',
        phone: patient.phone || '',
        address: patient.address || '',
        condition: patient.medical_condition || patient.condition || '',
        notes: patient.notes || '',
      });
    } else {
      setFormData({
        name: '',
        age: '',
        gender: '',
        phone: '',
        address: '',
        condition: '',
        notes: '',
      });
    }
  }, [patient, open]);

  const handleChange = (field) => (event) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };

  const handleSubmit = () => {
    onSave(formData);
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {patient ? t('editPatient') : t('addPatient')}
      </DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 1 }}>
          <TextField
            margin="dense"
            label={t('name')}
            fullWidth
            variant="outlined"
            value={formData.name}
            onChange={handleChange('name')}
            required
          />
          <TextField
            margin="dense"
            label={t('age')}
            fullWidth
            variant="outlined"
            type="number"
            value={formData.age}
            onChange={handleChange('age')}
            required
          />
          <FormControl fullWidth margin="dense">
            <InputLabel>{t('gender')}</InputLabel>
            <Select
              value={formData.gender}
              label={t('gender')}
              onChange={handleChange('gender')}
            >
              <MenuItem value="男">{t('male', '男')}</MenuItem>
              <MenuItem value="女">{t('female', '女')}</MenuItem>
            </Select>
          </FormControl>
          <TextField
            margin="dense"
            label={t('phone')}
            fullWidth
            variant="outlined"
            value={formData.phone}
            onChange={handleChange('phone')}
          />
          <TextField
            margin="dense"
            label={t('address')}
            fullWidth
            variant="outlined"
            multiline
            rows={2}
            value={formData.address}
            onChange={handleChange('address')}
          />
          <TextField
            margin="dense"
            label={t('condition')}
            fullWidth
            variant="outlined"
            multiline
            rows={3}
            value={formData.condition}
            onChange={handleChange('condition')}
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
          {patient ? t('save') : t('add')}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default PatientForm;
