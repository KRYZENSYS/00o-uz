import '../globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: '00o.uz — AI Platforma',
  description: 'O\'zbekistondagi eng katta AI platforma',
};

export default function LocaleLayout({ children, params }: { children: React.ReactNode; params: { locale: string } }) {
  return <div lang={params.locale}>{children}</div>;
}
