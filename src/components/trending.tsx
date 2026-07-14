"use client";
import { useTranslations } from "next-intl";
import { TrendingUp, Heart, Bookmark, ExternalLink } from "lucide-react";

const mockStartups = [
  { id: 1, name: "PayUz", category: "Fintech", logo: "💳", funding: "$250K", growth: "+180%" },
  { id: 2, name: "EduMaster", category: "EdTech", logo: "📚", funding: "$120K", growth: "+95%" },
  { id: 3, name: "AgroSmart", category: "AgriTech", logo: "🌾", funding: "$80K", growth: "+150%" },
  { id: 4, name: "HealthPlus", category: "HealthTech", logo: "🏥", funding: "$200K", growth: "+220%" },
  { id: 5, name: "LogiTrack", category: "Logistics", logo: "🚚", funding: "$150K", growth: "+110%" },
  { id: 6, name: "AIWriter", category: "AI", logo: "🤖", funding: "$300K", growth: "+340%" },
];

export function Trending() {
  const t = useTranslations("landing");
  return (
    <section className="relative px-4 py-20 max-w-7xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-6 h-6 text-purple-400" />
            <h2 className="text-3xl font-bold">{t("trending")}</h2>
          </div>
          <p className="text-gray-400">Eng ko'p ko'rilayotgan startaplar</p>
        </div>
        <a href="/startups" className="text-sm text-purple-400 hover:underline">{t("viewAll")}</a>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {mockStartups.map((s) => (
          <div key={s.id} className="glass rounded-2xl p-6 hover:bg-white/10 transition group">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500/30 to-pink-500/30 flex items-center justify-center text-2xl">
                  {s.logo}
                </div>
                <div>
                  <h3 className="font-semibold">{s.name}</h3>
                  <p className="text-xs text-gray-400">{s.category}</p>
                </div>
              </div>
              <span className="text-xs px-2 py-1 rounded-full bg-green-500/20 text-green-400">{s.growth}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-300">💰 {s.funding}</span>
              <div className="flex gap-3 text-gray-400">
                <button className="hover:text-pink-400 transition"><Heart className="w-4 h-4" /></button>
                <button className="hover:text-purple-400 transition"><Bookmark className="w-4 h-4" /></button>
                <a href={`/startups/${s.id}`} className="hover:text-white transition"><ExternalLink className="w-4 h-4" /></a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
