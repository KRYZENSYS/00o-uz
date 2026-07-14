import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: '00o.uz — O\'zbekistondagi eng katta AI platforma',
  description: 'AI Startap va Frilanser Habi | 30+ AI vosita, Startaplar, Ish, Xizmatlar, Kurslar',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="uz">
      <body className="bg-slate-900 text-white antialiased">{children}</body>
    </html>
  );
}
