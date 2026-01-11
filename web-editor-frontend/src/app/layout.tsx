import type { Metadata } from 'next';

import './globals.css';
import { AppProviders } from '@/components/AppProviders';

export const metadata: Metadata = {
  title: 'NextjsFastapiTextEditor',
  description: 'Upload → Convert → Edit (TipTap)',
  icons: {
    icon: [{ url: '/icon.svg', type: 'image/svg+xml' }]
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
