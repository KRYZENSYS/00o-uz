"use client";
import { useState, useEffect, createContext, useContext, ReactNode } from "react";

type Lang = "uz" | "ru" | "en";

const translations: Record<Lang, Record<string, string>> = {
  uz: {
    "app.name": "00o.uz", "app.tagline": "O'zbekistondagi eng katta AI platforma",
    "nav.home": "Bosh", "nav.startups": "Startaplar", "nav.jobs": "Ishlar", "nav.services": "Xizmatlar", "nav.ai": "AI",
    "auth.login": "Kirish", "auth.register": "Ro'yxatdan o'tish", "auth.logout": "Chiqish", "auth.profile": "Profil",
    "btn.search": "Qidirish", "btn.create": "Yaratish", "btn.save": "Saqlash", "btn.cancel": "Bekor qilish",
    "common.loading": "Yuklanmoqda...", "common.error": "Xatolik yuz berdi", "common.success": "Muvaffaqiyat",
    "home.hero.title": "Kelajak AI bilan bugun", "home.hero.subtitle": "30+ AI vosita, startaplar, ish o'rinlari, freelance xizmatlar",
    "home.cta.start": "AI bilan boshlash", "home.cta.explore": "Startaplarni ko'rish",
    "ai.tools": "AI vositalar", "ai.input.placeholder": "Savolingizni yozing...", "ai.output": "Natija",
    "startup.name": "Startap nomi", "startup.tagline": "Qisqa tavsif", "startup.category": "Soha", "startup.stage": "Bosqich",
    "premium.title": "Premium", "premium.month": "1 oy", "premium.year": "1 yil", "premium.lifetime": "Umrbod",
    "payment.payme": "Payme", "payment.click": "Click", "payment.uzum": "Uzum", "payment.stripe": "Visa/Master", "payment.ton": "TON",
  },
  ru: {
    "app.name": "00o.uz", "app.tagline": "Крупнейшая AI платформа в Узбекистане",
    "nav.home": "Главная", "nav.startups": "Стартапы", "nav.jobs": "Работа", "nav.services": "Услуги", "nav.ai": "AI",
    "auth.login": "Войти", "auth.register": "Регистрация", "auth.logout": "Выйти", "auth.profile": "Профиль",
    "btn.search": "Поиск", "btn.create": "Создать", "btn.save": "Сохранить", "btn.cancel": "Отмена",
    "common.loading": "Загрузка...", "common.error": "Произошла ошибка", "common.success": "Успешно",
    "home.hero.title": "Будущее с AI сегодня", "home.hero.subtitle": "30+ AI инструментов, стартапы, вакансии, фриланс услуги",
    "home.cta.start": "Начать с AI", "home.cta.explore": "Смотреть стартапы",
    "ai.tools": "AI инструменты", "ai.input.placeholder": "Напишите ваш вопрос...", "ai.output": "Результат",
    "startup.name": "Название стартапа", "startup.tagline": "Краткое описание", "startup.category": "Категория", "startup.stage": "Этап",
    "premium.title": "Премиум", "premium.month": "1 месяц", "premium.year": "1 год", "premium.lifetime": "Навсегда",
    "payment.payme": "Payme", "payment.click": "Click", "payment.uzum": "Uzum", "payment.stripe": "Visa/Master", "payment.ton": "TON",
  },
  en: {
    "app.name": "00o.uz", "app.tagline": "The largest AI platform in Uzbekistan",
    "nav.home": "Home", "nav.startups": "Startups", "nav.jobs": "Jobs", "nav.services": "Services", "nav.ai": "AI",
    "auth.login": "Login", "auth.register": "Sign up", "auth.logout": "Logout", "auth.profile": "Profile",
    "btn.search": "Search", "btn.create": "Create", "btn.save": "Save", "btn.cancel": "Cancel",
    "common.loading": "Loading...", "common.error": "An error occurred", "common.success": "Success",
    "home.hero.title": "The future with AI today", "home.hero.subtitle": "30+ AI tools, startups, jobs, freelance services",
    "home.cta.start": "Start with AI", "home.cta.explore": "Explore startups",
    "ai.tools": "AI tools", "ai.input.placeholder": "Type your question...", "ai.output": "Result",
    "startup.name": "Startup name", "startup.tagline": "Short description", "startup.category": "Category", "startup.stage": "Stage",
    "premium.title": "Premium", "premium.month": "1 month", "premium.year": "1 year", "premium.lifetime": "Lifetime",
    "payment.payme": "Payme", "payment.click": "Click", "payment.uzum": "Uzum", "payment.stripe": "Visa/Master", "payment.ton": "TON",
  }
};

const I18nContext = createContext<{ t: (k: string) => string; lang: Lang; setLang: (l: Lang) => void }>({ t: (k) => k, lang: "uz", setLang: () => {} });

export function I18nProvider({ children }: { children: ReactNode }) {
  const [lang, setLangState] = useState<Lang>("uz");
  useEffect(() => { const saved = localStorage.getItem("lang") as Lang; if (saved && translations[saved]) setLangState(saved); }, []);
  const setLang = (l: Lang) => { setLangState(l); localStorage.setItem("lang", l); };
  const t = (k: string) => translations[lang][k] || translations.uz[k] || k;
  return <I18nContext.Provider value={{ t, lang, setLang }}>{children}</I18nContext.Provider>;
}

export const useI18n = () => useContext(I18nContext);
