import React, { createContext, useContext, useState, useEffect } from 'react';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage必须在LanguageProvider中使用');
  }
  return context;
};

export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState('zh');
  const [translations, setTranslations] = useState({});

  // 定义支持的语言
  const languages = {
    zh: { code: 'zh', name: '中文', flag: '🇨🇳' },
    en: { code: 'en', name: 'English', flag: '🇺🇸' },
    ja: { code: 'ja', name: '日本語', flag: '🇯🇵' }
  };

  // 加载翻译文件
  useEffect(() => {
    const loadTranslations = async (langCode) => {
      try {
        const response = await fetch(`/locales/${langCode}/translation.json`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setTranslations(prev => ({
          ...prev,
          [langCode]: data
        }));
      } catch (error) {
        console.error(`Failed to load translations for ${langCode}:`, error);
        // 如果加载失败，使用默认的内联翻译
        setTranslations(prev => ({
          ...prev,
          [langCode]: getDefaultTranslations(langCode)
        }));
      }
    };

    // 预加载所有语言的翻译
    Object.keys(languages).forEach(langCode => {
      if (!translations[langCode]) {
        loadTranslations(langCode);
      }
    });
  }, []);

  // 默认翻译（如果JSON加载失败）
  const getDefaultTranslations = (langCode) => {
    const defaults = {
      zh: {
        title: 'HospitalRun - 医院管理系统',
        dashboard: '仪表板',
        patients: '患者管理',
        appointments: '预约管理',
        doctors: '医生管理',
      },
      en: {
        title: 'HospitalRun - Hospital Management System',
        dashboard: 'Dashboard',
        patients: 'Patient Management',
        appointments: 'Appointment Management',
        doctors: 'Doctor Management',
      },
      ja: {
        title: 'HospitalRun - 病院管理システム',
        dashboard: 'ダッシュボード',
        patients: '患者管理',
        appointments: '予約管理',
        doctors: '医師管理',
      }
    };
    return defaults[langCode] || defaults.zh;
  };

  // 翻译函数
  const t = (key) => {
    const langTexts = translations[currentLanguage];
    if (langTexts && langTexts[key]) {
      return langTexts[key];
    }

    // 如果当前语言的翻译不存在或没有找到键，返回默认值
    const fallbackTexts = translations.zh;
    if (fallbackTexts && fallbackTexts[key]) {
      return fallbackTexts[key];
    }

    // 如果都找不到，返回键本身
    return key;
  };

  const changeLanguage = (langCode) => {
    if (languages[langCode]) {
      setCurrentLanguage(langCode);
    } else {
      console.warn(`Language ${langCode} is not supported`);
    }
  };

  const value = {
    currentLanguage,
    languages,
    changeLanguage,
    t,
    translations,
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};

export default LanguageContext;
