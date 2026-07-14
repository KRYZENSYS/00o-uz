"use client";
import { useRouter, usePathname } from "next/navigation";
import { Globe } from "lucide-react";
import { useState } from "react";

const languages = [
  { code: "uz", name: "O'zbek", flag: "🇺🇿" },
  { code: "ru", name: "Русский", flag: "🇷🇺" },
  { code: "en", name: "English", flag: "🇬🇧" },
];

export function LanguageSwitcher() {
  const router = useRouter();
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  const switchLang = (code: string) => {
    const newPath = pathname.replace(/^\/(uz|ru|en)/, `/${code}`);
    document.cookie = `NEXT_LOCALE=${code}; path=/; max-age=31536000`;
    localStorage.setItem("locale", code);
    router.push(newPath);
    setOpen(false);
  };

  return (
    <div className="relative">
      <button onClick={() => setOpen(!open)} className="p-2 rounded-lg glass hover:bg-white/10 transition">
        <Globe className="w-4 h-4" />
      </button>
      {open && (
        <div className="absolute right-0 mt-2 w-40 rounded-xl glass-strong p-2 z-50">
          {languages.map((lang) => (
            <button key={lang.code} onClick={() => switchLang(lang.code)}
              className="w-full text-left px-3 py-2 rounded-lg hover:bg-white/10 transition flex items-center gap-2 text-sm">
              <span>{lang.flag}</span>
              <span>{lang.name}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
