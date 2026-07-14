"use client";
import { useState, useEffect } from "react";
import { BarChart3, Users, Rocket, Briefcase, Wrench, TrendingUp, Sparkles, Eye, Heart, Crown } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function AnalyticsPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  const load = async () => {
    const t = localStorage.getItem("token");
    try { const r = await fetch(`${API_URL}/api/v1/analytics/dashboard`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setData(await r.json()); } catch {}
    setLoading(false);
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white"><div className="w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin"></div></div>;
  if (!data) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">Ma'lumot yo'q</div>;

  const stats = [
    { l: "Startaplar", v: data.startups, icon: Rocket, c: "from-blue-500 to-cyan-500" },
    { l: "Ishlar", v: data.jobs, icon: Briefcase, c: "from-green-500 to-emerald-500" },
    { l: "Xizmatlar", v: data.services, icon: Wrench, c: "from-yellow-500 to-orange-500" },
    { l: "AI so'rovlar", v: data.ai_requests_total, icon: Sparkles, c: "from-purple-500 to-pink-500" },
    { l: "Bu hafta AI", v: data.ai_requests_week, icon: TrendingUp, c: "from-pink-500 to-rose-500" },
    { l: "Token ishlatilgan", v: data.ai_tokens_used, icon: Eye, c: "from-indigo-500 to-purple-500" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-cyan-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-5xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold flex items-center gap-3"><BarChart3 className="w-10 h-10 text-cyan-400" /> Analitika</h1>
          <p className="text-gray-400 mt-2">Faoliyatingiz statistikasi</p>
        </div>

        <div className="bg-gradient-to-br from-yellow-500/20 to-orange-500/20 border border-yellow-500/30 rounded-2xl p-5 mb-6 flex items-center gap-4">
          <Crown className="w-12 h-12 text-yellow-400" />
          <div className="flex-1">
            <div className="font-bold text-lg">Premium holat: {data.is_premium ? "✅ Faol" : "❌ Faol emas"}</div>
            {data.premium_expires && <div className="text-sm text-gray-300">Tugaydi: {new Date(data.premium_expires).toLocaleDateString()}</div>}
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-yellow-400">{data.tokens_balance}</div>
            <div className="text-xs text-gray-400">Token</div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {stats.map((s, i) => { const Icon = s.icon; return (
            <div key={i} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${s.c} flex items-center justify-center mb-3`}><Icon className="w-6 h-6" /></div>
              <div className="text-3xl font-extrabold">{s.v}</div>
              <div className="text-sm text-gray-400">{s.l}</div>
            </div>
          );})}
        </div>
      </div>
    </div>
  );
}
