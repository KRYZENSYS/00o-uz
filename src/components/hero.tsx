"use client";
import { useTranslations } from "next-intl";
import { Search, Sparkles, Rocket, Users, Briefcase } from "lucide-react";

export function Hero() {
  const t = useTranslations("landing.hero");
  return (
    <section className="relative px-4 py-20 sm:py-32 max-w-7xl mx-auto">
      <div className="text-center max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8">
          <Sparkles className="w-4 h-4 text-purple-400" />
          <span className="text-sm">Powered by AI · GroqCloud</span>
        </div>
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight mb-6">
          <span className="gradient-text">{t("title")}</span>
        </h1>
        <p className="text-lg sm:text-xl text-gray-300 mb-12 max-w-2xl mx-auto">{t("subtitle")}</p>
        <div className="relative max-w-2xl mx-auto mb-12">
          <div className="glass-strong rounded-2xl p-2 flex items-center gap-2 glow">
            <Search className="w-5 h-5 ml-3 text-purple-400" />
            <input type="text" placeholder={t("searchPlaceholder")}
              className="flex-1 bg-transparent outline-none px-3 py-3 text-white placeholder:text-gray-400" />
            <button className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 font-medium hover:opacity-90 transition">
              Search
            </button>
          </div>
        </div>
        <div className="flex flex-wrap justify-center gap-4">
          <a href="/startups/create" className="px-6 py-3 rounded-xl glass hover:bg-white/10 transition flex items-center gap-2">
            <Rocket className="w-4 h-4" /> Create Startup
          </a>
          <a href="/freelancers/services" className="px-6 py-3 rounded-xl glass hover:bg-white/10 transition flex items-center gap-2">
            <Briefcase className="w-4 h-4" /> Find Work
          </a>
          <a href="/teams" className="px-6 py-3 rounded-xl glass hover:bg-white/10 transition flex items-center gap-2">
            <Users className="w-4 h-4" /> Find Team
          </a>
        </div>
      </div>
    </section>
  );
}
