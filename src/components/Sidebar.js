import React from 'react';
import { Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import PeopleIcon from '@mui/icons-material/People';
import EventNoteIcon from '@mui/icons-material/EventNote';
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import { useLanguage } from '../contexts/LanguageContext';

const Sidebar = ({ open, onClose, onNavigate }) => {
  const { t } = useLanguage();

  const menuItems = [
    { text: t('dashboard'), icon: <DashboardIcon />, path: '/' },
    { text: t('patients'), icon: <PeopleIcon />, path: '/patients' },
    { text: t('appointments'), icon: <EventNoteIcon />, path: '/appointments' },
    { text: t('doctors'), icon: <ManageAccountsIcon />, path: '/doctors' },
  ];

  return (
    <Drawer anchor="left" open={open} onClose={onClose}>
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton onClick={() => onNavigate(item.path)}>
              <ListItemIcon>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;
