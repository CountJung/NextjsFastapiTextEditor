'use client';

import { CssBaseline, ThemeProvider } from '@mui/material';

import { useAppTheme } from '@/lib/useAppTheme';

export function AppProviders({ children }: { children: React.ReactNode }) {
  const theme = useAppTheme();

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}
