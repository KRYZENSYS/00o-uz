"use client";
import { useTranslations } from "next-intl";
import { Rocket, Users, DollarSign, Briefcase } from "lucide-react";

export function Stats() {
  const t = useTranslations("landing.stats");
  const stats = [
    { icon: Rocket, label: t("startups"), value: "1,250+", color: "from-purple-500 to-pink-500" },
    { icon: Users, label: t("freelancers"), value: "5,800+", color: "from-blue-500 to-cyan-500" },
    { icon: DollarSign, label: t("investors"), value: "320+", color: "from-green-500 to-emerald-500" },
    { icon: Briefcase, label: t("jobs"), value: "890+", color: "from-orange-500 to-red-500" },
  ];
  return (
    <section className="relative px-4 py-16 max-w-7xl mx-auto">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((s, i) => (
          <div key={i} className="glass rounded-2xl p-6 hover:bg-white/10 transition">
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${s.color} flex items-center justify-center mb-3`}>
              <s.icon className="w-6 h-6 text-white" />
            </div>
            <div className="text-3xl font-bold mb-1">{s.value}</div>
            <div className="text-sm text-gray-400">{s.label}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
