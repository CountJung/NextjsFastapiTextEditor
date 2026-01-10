'use client';

import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import SettingsBrightnessIcon from '@mui/icons-material/SettingsBrightness';
import { IconButton, Tooltip } from '@mui/material';

import { getStoredThemeMode, setStoredThemeMode, type ThemeMode } from '@/lib/themeModeStorage';
import { useEffect, useState } from 'react';

function nextMode(mode: ThemeMode): ThemeMode {
  if (mode === 'system') return 'light';
  if (mode === 'light') return 'dark';
  return 'system';
}

export function ThemeModeToggle() {
  const [mode, setMode] = useState<ThemeMode>('system');

  useEffect(() => {
    setMode(getStoredThemeMode());
  }, []);

  const icon =
    mode === 'dark' ? <DarkModeIcon /> : mode === 'light' ? <LightModeIcon /> : <SettingsBrightnessIcon />;
  const label = mode === 'dark' ? '다크' : mode === 'light' ? '라이트' : '시스템';

  return (
    <Tooltip title={`테마: ${label} (클릭하여 변경)`}>
      <IconButton
        color="inherit"
        onClick={() => {
          const updated = nextMode(mode);
          setMode(updated);
          setStoredThemeMode(updated);
          window.dispatchEvent(new Event('themeModeChanged'));
        }}
      >
        {icon}
      </IconButton>
    </Tooltip>
  );
}
