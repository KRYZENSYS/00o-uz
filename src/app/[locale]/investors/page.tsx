"use client";
import { useState, useEffect } from "react";
import { TrendingUp, DollarSign, MapPin, Globe, Award, Filter, Search, BadgeCheck } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function InvestorsPage() {
  const [investors, setInvestors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [type, setType] = useState("");

  useEffect(() => { load(); }, [type]);

  const load = async () => {
    setLoading(true);
    const p = new URLSearchParams();
    if (search) p.append("search", search);
    if (type) p.append("type", type);
    try {
      const r = await fetch(`${API_URL}/api/v1/investors/?${p}`);
      setInvestors(await r.json());
    } catch {}
    setLoading(false);
  };

  const format = (n: number) => n >= 1000000 ? `$${(n/1000000).toFixed(1)}M` : n >= 1000 ? `$${(n/1000).toFixed(0)}K` : `$${n}`;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-green-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold flex items-center gap-3"><TrendingUp className="w-10 h-10 text-green-400" /> Investorlar</h1>
          <p className="text-gray-400 mt-2">O'zbekistondagi investorlar va fondlar</p>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6 flex flex-wrap gap-3">
          <div className="flex-1 min-w-[200px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && load()}
              placeholder="Investor qidirish..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-green-500 focus:outline-none" />
          </div>
          <select value={type} onChange={(e) => setType(e.target.value)} className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
            <option value="">Barcha turlar</option>
            <option value="angel">Angel investor</option>
            <option value="vc">Venture Capital</option>
            <option value="fund">Fond</option>
            <option value="accelerator">Akselerator</option>
            <option value="syndicate">Sindikat</option>
          </select>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-green-500 border-t-transparent rounded-full animate-spin"></div></div> :
        investors.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><TrendingUp className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">Investorlar topilmadi</p></div> :
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {investors.map(i => (
            <div key={i.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 hover:border-green-500/50 transition">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center text-2xl font-bold">{i.name[0]}</div>
                  <div>
                    <h3 className="font-bold text-lg flex items-center gap-1">{i.name} {i.is_verified && <BadgeCheck className="w-4 h-4 text-blue-400" />}</h3>
                    <span className="text-sm text-gray-400 capitalize">{i.type}</span>
                  </div>
                </div>
                {i.is_featured && <span className="px-2 py-0.5 bg-yellow-500/20 text-yellow-400 text-xs rounded-full">⭐ Top</span>}
              </div>
              <p className="text-gray-300 text-sm mb-3 line-clamp-2">{i.bio}</p>
              {i.industries?.length > 0 && (
                <div className="flex flex-wrap gap-1 mb-3">{i.industries.slice(0, 4).map((s: string) => <span key={s} className="px-2 py-0.5 bg-white/5 text-xs rounded text-gray-300">{s}</span>)}</div>
              )}
              <div className="grid grid-cols-3 gap-2 border-t border-white/10 pt-3">
                <div><div className="text-xs text-gray-400">Investitsiya</div><div className="font-bold text-green-400">{format(i.min_investment)} - {format(i.max_investment)}</div></div>
                <div><div className="text-xs text-gray-400">Portfolio</div><div className="font-bold">{i.portfolio_count}</div></div>
                <div><div className="text-xs text-gray-400">Jami</div><div className="font-bold">{format(i.total_invested)}</div></div>
              </div>
              <button className="w-full mt-3 py-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl font-medium text-sm">Murojaat qilish</button>
            </div>
          ))}
        </div>}
      </div>
    </div>
  );
}
