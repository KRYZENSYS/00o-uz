"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { Rocket, TrendingUp, MapPin, Heart, Eye, Plus, Search, Filter } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function StartupsPage() {
  const [startups, setStartups] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [stage, setStage] = useState("");

  useEffect(() => { load(); }, [category, stage]);

  const load = async () => {
    setLoading(true);
    const p = new URLSearchParams();
    if (search) p.append("search", search);
    if (category) p.append("category", category);
    if (stage) p.append("stage", stage);
    try { const r = await fetch(`${API_URL}/api/v1/startups/?${p}`); setStartups(await r.json()); } catch {}
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
          <div>
            <h1 className="text-4xl font-bold flex items-center gap-3"><Rocket className="w-10 h-10 text-purple-400" /> Startaplar</h1>
            <p className="text-gray-400 mt-1">O'zbekistondagi eng yaxshi startaplar</p>
          </div>
          <Link href="/startups/new" className="px-5 py-2.5 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl font-medium flex items-center gap-2"><Plus className="w-4 h-4" /> Yangi startap</Link>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6 flex flex-wrap gap-3">
          <div className="flex-1 min-w-[200px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && load()}
              placeholder="Startap qidirish..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-purple-500 focus:outline-none" />
          </div>
          <select value={category} onChange={(e) => setCategory(e.target.value)} className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
            <option value="">Barcha sohalar</option>
            <option value="fintech">Fintex</option>
            <option value="edtech">Edtex</option>
            <option value="healthtech">Sog'liq</option>
            <option value="ecommerce">E-commerce</option>
            <option value="saas">SaaS</option>
            <option value="ai">AI</option>
            <option value="logistics">Logistika</option>
            <option value="agtech">Agro</option>
            <option value="marketplace">Marketpleys</option>
          </select>
          <select value={stage} onChange={(e) => setStage(e.target.value)} className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
            <option value="">Barcha bosqichlar</option>
            <option value="idea">G'oya</option>
            <option value="mvp">MVP</option>
            <option value="seed">Seed</option>
            <option value="series_a">Series A</option>
            <option value="series_b">Series B</option>
            <option value="growth">O'sish</option>
          </select>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div></div> :
        startups.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><Rocket className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">Startaplar topilmadi</p></div> :
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {startups.map(s => (
            <Link key={s.id} href={`/startups/${s.id}`} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden hover:border-purple-500/50 transition group">
              <div className="h-32 bg-gradient-to-br from-purple-500 via-pink-500 to-red-500 relative">
                {s.is_featured && <div className="absolute top-3 right-3 px-2 py-0.5 bg-yellow-500 text-black text-xs rounded-full font-bold">⭐ Top</div>}
                {s.is_verified && <div className="absolute top-3 left-3 px-2 py-0.5 bg-blue-500 text-white text-xs rounded-full font-bold">✓ Verified</div>}
                <div className="absolute -bottom-8 left-4 w-16 h-16 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 border-4 border-slate-900 flex items-center justify-center text-2xl font-bold">{s.name[0]}</div>
              </div>
              <div className="p-4 pt-10">
                <h3 className="font-bold text-lg mb-1 group-hover:text-purple-400 transition">{s.name}</h3>
                <p className="text-gray-400 text-sm line-clamp-2 mb-3">{s.tagline}</p>
                <div className="flex flex-wrap gap-1 mb-3">
                  <span className="px-2 py-0.5 bg-purple-500/20 text-purple-300 text-xs rounded">{s.category}</span>
                  <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 text-xs rounded">{s.stage}</span>
                </div>
                <div className="flex items-center gap-3 text-xs text-gray-400">
                  <span className="flex items-center gap-1"><Eye className="w-3 h-3" />{s.views_count}</span>
                  <span className="flex items-center gap-1"><Heart className="w-3 h-3" />{s.likes_count}</span>
                  {s.location && <span className="flex items-center gap-1"><MapPin className="w-3 h-3" />{s.location}</span>}
                </div>
              </div>
            </Link>
          ))}
        </div>}
      </div>
    </div>
  );
}
