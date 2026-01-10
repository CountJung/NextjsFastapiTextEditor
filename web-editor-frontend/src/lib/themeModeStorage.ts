export type ThemeMode = 'system' | 'light' | 'dark';

const KEY = 'themeMode';

export function getStoredThemeMode(): ThemeMode {
  if (typeof window === 'undefined') return 'system';
  const raw = window.localStorage.getItem(KEY);
  if (raw === 'light' || raw === 'dark' || raw === 'system') return raw;
  return 'system';
}

export function setStoredThemeMode(mode: ThemeMode) {
  window.localStorage.setItem(KEY, mode);
}
