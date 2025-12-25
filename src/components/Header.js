import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, Box, Button } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { useLanguage } from '../contexts/LanguageContext';

const Header = ({ onMenuClick }) => {
  const { currentLanguage, languages, changeLanguage, t } = useLanguage();

  const handleLanguageChange = (langCode) => {
    changeLanguage(langCode);
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
          onClick={onMenuClick}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          {t('title')}
        </Typography>

        {/* 语言切换按钮 */}
        <Box sx={{ display: 'flex', gap: 1 }}>
          {Object.values(languages).map((lang) => (
            <Button
              key={lang.code}
              variant={currentLanguage === lang.code ? 'contained' : 'text'}
              color="inherit"
              size="small"
              onClick={() => handleLanguageChange(lang.code)}
              sx={{ minWidth: 'auto', px: 1 }}
              title={lang.name}
            >
              {lang.flag}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
