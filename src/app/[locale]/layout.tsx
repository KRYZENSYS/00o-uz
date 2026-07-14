import type { Metadata } from "next";
import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";
import { notFound } from "next/navigation";
import { locales } from "@/i18n/request";
import "../globals.css";

export const metadata: Metadata = {
  title: "00o.uz - AI Startup & Freelancer Hub",
  description: "O'zbekistondagi eng katta startup, frilanser va investor platformasi",
  keywords: ["startup", "freelancer", "investor", "AI", "O'zbekiston", "00o.uz"],
};

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export default async function LocaleLayout({
  children, params,
}: { children: React.ReactNode; params: Promise<{ locale: string }>; }) {
  const { locale } = await params;
  if (!locales.includes(locale as any)) notFound();
  const messages = await getMessages();
  return (
    <html lang={locale} suppressHydrationWarning>
      <body className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 text-white antialiased">
        <NextIntlClientProvider messages={messages}>{children}</NextIntlClientProvider>
      </body>
    </html>
  );
}
