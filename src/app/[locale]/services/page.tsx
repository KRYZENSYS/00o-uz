"use client";
import { useState, useEffect } from "react";
import { Wrench, Search, Star, Clock, Tag, ShoppingCart, X } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ServicesPage() {
  const [services, setServices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [selected, setSelected] = useState<any>(null);

  useEffect(() => { load(); }, [category]);

  const load = async () => {
    setLoading(true);
    const p = new URLSearchParams();
    if (search) p.append("search", search);
    if (category) p.append("category", category);
    try {
      const r = await fetch(`${API_URL}/api/v1/services?${p}`);
      setServices(await r.json());
    } catch {}
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-orange-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold flex items-center gap-3"><Wrench className="w-10 h-10 text-yellow-400" /> Freelance Xizmatlar</h1>
          <p className="text-gray-400 mt-2">Professional mutaxassislar xizmati</p>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6 flex flex-wrap gap-3">
          <div className="flex-1 min-w-[200px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && load()}
              placeholder="Xizmat qidirish..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-yellow-500 focus:outline-none" />
          </div>
          <select value={category} onChange={(e) => setCategory(e.target.value)} className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
            <option value="">Barcha kategoriyalar</option>
            <option value="design">Dizayn</option>
            <option value="development">Dasturlash</option>
            <option value="marketing">Marketing</option>
            <option value="writing">Kontent</option>
            <option value="video">Video</option>
            <option value="audio">Audio</option>
            <option value="business">Biznes</option>
          </select>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-yellow-500 border-t-transparent rounded-full animate-spin"></div></div> :
        services.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><Wrench className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">Xizmatlar topilmadi</p></div> :
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {services.map((s) => (
            <div key={s.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 hover:border-yellow-500/50 transition cursor-pointer" onClick={() => setSelected(s)}>
              <div className="flex items-center justify-between mb-3">
                {s.is_featured && <span className="px-2 py-0.5 bg-yellow-500/20 text-yellow-400 text-xs rounded-full">⭐ Top</span>}
                <div className="flex items-center gap-1 text-sm text-yellow-400"><Star className="w-4 h-4 fill-yellow-400" />{s.rating || "5.0"}</div>
              </div>
              <h3 className="font-bold text-lg mb-2 line-clamp-2">{s.title}</h3>
              <p className="text-gray-400 text-sm mb-3 line-clamp-2">{s.description}</p>
              <div className="flex flex-wrap gap-1 mb-4">
                {s.tags?.slice(0, 3).map((t: string) => <span key={t} className="px-2 py-0.5 bg-white/5 text-xs rounded text-gray-300">{t}</span>)}
              </div>
              <div className="flex items-end justify-between border-t border-white/10 pt-3">
                <div>
                  <div className="text-xs text-gray-400">Boshlanadi</div>
                  <div className="text-2xl font-bold text-yellow-400">{Math.round(s.price_basic).toLocaleString()} so'm</div>
                </div>
                <div className="text-xs text-gray-400 flex items-center gap-1"><Clock className="w-3 h-3" />{s.delivery_days} kun</div>
              </div>
            </div>
          ))}
        </div>}
      </div>

      {selected && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onClick={() => setSelected(null)}>
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-3xl w-full max-h-[85vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-2xl font-bold mb-1">{selected.title}</h2>
                <div className="flex items-center gap-2 text-sm text-gray-400">
                  <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" /> {selected.rating} • {selected.orders_count} buyurtma • {selected.delivery_days} kun
                </div>
              </div>
              <button onClick={() => setSelected(null)}><X className="w-6 h-6" /></button>
            </div>
            <p className="text-gray-300 mb-4 whitespace-pre-wrap">{selected.description}</p>
            <div className="grid md:grid-cols-3 gap-3">
              {[
                { name: "Basic", price: selected.price_basic, desc: "Boshlang'ich paket" },
                { name: "Standard", price: selected.price_standard, desc: "O'rtacha paket" },
                { name: "Premium", price: selected.price_premium, desc: "To'liq paket" }
              ].filter(p => p.price).map((p) => (
                <div key={p.name} className="bg-white/5 border border-white/10 rounded-xl p-4 text-center">
                  <div className="text-sm text-gray-400">{p.name}</div>
                  <div className="text-2xl font-bold text-yellow-400 my-2">{Math.round(p.price).toLocaleString()} so'm</div>
                  <div className="text-xs text-gray-500 mb-3">{p.desc}</div>
                  <button className="w-full py-2 bg-yellow-500 text-black rounded-lg text-sm font-bold flex items-center justify-center gap-1">
                    <ShoppingCart className="w-4 h-4" /> Buyurtma
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
