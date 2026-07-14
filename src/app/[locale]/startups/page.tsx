"use client";
import { useState, useEffect } from "react";
import { Rocket, Search, Heart, Eye, MapPin } from "lucide-react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function StartupsPage() {
  const [startups, setStartups] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");

  useEffect(() => { load(); }, [category]);

  const load = async () => {
    setLoading(true);
    try {
      const p = new URLSearchParams();
      if (category) p.append("category", category);
      if (search) p.append("search", search);
      const r = await fetch(`${API_URL}/api/v1/startups?${p}`);
      setStartups(await r.json());
    } catch {}
    setLoading(false);
  };

  const like = async (id: number) => {
    await fetch(`${API_URL}/api/v1/startups/${id}/like`, { method: "POST" });
    load();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold flex items-center gap-3"><Rocket className="w-10 h-10 text-purple-400" /> Startaplar</h1>
            <p className="text-gray-400 mt-2">O'zbekistondagi eng yaxshi startaplar</p>
          </div>
          <Link href="/startups/create" className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl font-semibold">+ Yangi</Link>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6 flex flex-wrap gap-3">
          <div className="flex-1 min-w-[200px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && load()}
              placeholder="Qidirish..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-purple-500 focus:outline-none" />
          </div>
          <select value={category} onChange={(e) => setCategory(e.target.value)} className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
            <option value="">Barcha</option>
            <option value="fintech">Fintech</option>
            <option value="edtech">Edtech</option>
            <option value="ai">AI/ML</option>
            <option value="saas">SaaS</option>
            <option value="ecommerce">E-commerce</option>
            <option value="healthtech">Healthtech</option>
          </select>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div></div> :
        startups.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><Rocket className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">Hozircha startaplar yo'q</p></div> :
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {startups.map((s) => (
            <div key={s.id} className="group bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-purple-500/50 transition-all">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-14 h-14 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center text-2xl font-bold">{s.name[0]}</div>
                  <div>
                    <h3 className="font-bold text-lg flex items-center gap-1">{s.name}{s.is_verified && <span className="text-blue-400">✓</span>}</h3>
                    <span className="text-xs text-purple-400 uppercase">{s.stage}</span>
                  </div>
                </div>
                {s.is_featured && <span className="px-2 py-1 bg-yellow-500/20 text-yellow-400 text-xs rounded-full">⭐</span>}
              </div>
              <p className="text-gray-300 text-sm mb-4 line-clamp-2">{s.tagline}</p>
              <div className="flex flex-wrap gap-2 mb-4">
                <span className="px-2 py-1 bg-white/5 text-xs rounded-lg">{s.category}</span>
                {s.location && <span className="px-2 py-1 bg-white/5 text-xs rounded-lg flex items-center gap-1"><MapPin className="w-3 h-3" />{s.location}</span>}
              </div>
              <div className="flex items-center justify-between pt-4 border-t border-white/10">
                <div className="flex items-center gap-4 text-sm text-gray-400">
                  <span className="flex items-center gap-1"><Eye className="w-4 h-4" />{s.views_count}</span>
                  <button onClick={() => like(s.id)} className="flex items-center gap-1 hover:text-pink-400"><Heart className="w-4 h-4" />{s.likes_count}</button>
                </div>
                <Link href={`/startups/${s.id}`} className="text-purple-400 text-sm font-medium">Batafsil →</Link>
              </div>
            </div>
          ))}
        </div>}
      </div>
    </div>
  );
}
