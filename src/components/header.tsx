"use client";
import { useTranslations } from "next-intl";
import { Menu, X, Sparkles } from "lucide-react";
import { useState } from "react";
import Link from "next/link";
import { LanguageSwitcher } from "./language-switcher";

export function Header() {
  const t = useTranslations("nav");
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-50 glass border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center glow">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold gradient-text">00o.uz</span>
          </Link>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/startups" className="text-sm hover:text-purple-400 transition">{t("startups")}</Link>
            <Link href="/freelancers" className="text-sm hover:text-purple-400 transition">{t("freelancers")}</Link>
            <Link href="/investors" className="text-sm hover:text-purple-400 transition">{t("investors")}</Link>
            <Link href="/jobs" className="text-sm hover:text-purple-400 transition">{t("jobs")}</Link>
            <Link href="/ai" className="text-sm hover:text-purple-400 transition flex items-center gap-1">
              <Sparkles className="w-4 h-4" /> {t("ai")}
            </Link>
          </nav>
          <div className="hidden md:flex items-center gap-3">
            <LanguageSwitcher />
            <Link href="/login" className="text-sm hover:text-purple-400 transition">{t("signIn")}</Link>
            <Link href="/register" className="px-4 py-2 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 text-sm font-medium hover:opacity-90 transition">
              {t("getStarted")}
            </Link>
          </div>
          <button className="md:hidden" onClick={() => setOpen(!open)}>
            {open ? <X /> : <Menu />}
          </button>
        </div>
      </div>
    </header>
  );
}
