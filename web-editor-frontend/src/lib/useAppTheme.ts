'use client';

import { createTheme, useMediaQuery } from '@mui/material';
import { useEffect, useMemo, useState } from 'react';

import { getStoredThemeMode, type ThemeMode } from '@/lib/themeModeStorage';

export function useAppTheme() {
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)');
  const [mode, setMode] = useState<ThemeMode>('system');

  useEffect(() => {
    const read = () => setMode(getStoredThemeMode());
    read();
    window.addEventListener('themeModeChanged', read);
    return () => window.removeEventListener('themeModeChanged', read);
  }, []);

  const paletteMode = mode === 'system' ? (prefersDark ? 'dark' : 'light') : mode;

  return useMemo(
    () =>
      createTheme({
        palette: {
          mode: paletteMode
        }
      }),
    [paletteMode]
  );
}
