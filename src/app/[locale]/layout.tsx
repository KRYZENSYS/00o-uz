"use client";
import { ReactNode } from "react";
import Navbar from "@/components/Navbar";
import { TelegramWebApp } from "@/components/TelegramWebApp";

export default function LocaleLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen">
      <TelegramWebApp />
      <Navbar />
      <main>{children}</main>
      <footer className="border-t border-white/10 bg-slate-900/50 backdrop-blur mt-20 py-8 px-4 text-center text-sm text-gray-400">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-center gap-6 mb-3 flex-wrap">
            <a href="/about" className="hover:text-white">Biz haqimizda</a>
            <a href="/terms" className="hover:text-white">Foydalanish shartlari</a>
            <a href="/privacy" className="hover:text-white">Maxfiylik</a>
            <a href="https://t.me/oo0o_uz" className="hover:text-white">Telegram</a>
          </div>
          <div>© 2026 00o.uz — O'zbekistondagi eng katta AI platforma</div>
        </div>
      </footer>
    </div>
  );
}
