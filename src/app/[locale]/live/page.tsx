"use client";
import { useState, useEffect } from "react";
import { Video, Play, Users, Eye, Calendar, Heart, Radio, Plus, Clock, X, Gift } from "lucide-react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function LivePage() {
  const [tab, setTab] = useState<"live" | "upcoming" | "past">("live");
  const [streams, setStreams] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showSchedule, setShowSchedule] = useState(false);

  useEffect(() => { load(); }, [tab]);

  const load = async () => {
    setLoading(true);
    const url = tab === "live" ? "/streams/live" : tab === "upcoming" ? "/streams/upcoming" : "/streams/past";
    try { const r = await fetch(`${API_URL}/api/v1${url}`); if (r.ok) setStreams(await r.json()); } catch {}
    setLoading(false);
  };

  const join = async (id: number) => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    const r = await fetch(`${API_URL}/api/v1/streams/${id}/join`, { method: "POST", headers: { Authorization: `Bearer ${t}` } });
    if (r.ok) { const d = await r.json(); window.open(d.playback_url, "_blank"); }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-red-900 to-slate-900 text-white p-4 md:p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
          <div>
            <h1 className="text-4xl font-bold flex items-center gap-3"><Radio className="w-10 h-10 text-red-400 animate-pulse" /> Live</h1>
            <p className="text-gray-400 mt-1">Jonli efirlar, vebinarlar, onlayn uchrashuvlar</p>
          </div>
          <button onClick={() => setShowSchedule(true)} className="px-5 py-2.5 bg-gradient-to-r from-red-500 to-pink-500 rounded-xl font-medium flex items-center gap-2"><Plus className="w-4 h-4" /> Efir boshlash</button>
        </div>

        <div className="flex gap-2 mb-6 bg-white/5 p-1 rounded-xl">
          {[
            { id: "live", name: "🔴 Jonli", icon: Radio },
            { id: "upcoming", name: "📅 Rejalashtirilgan", icon: Calendar },
            { id: "past", name: "📼 O'tgan", icon: Clock },
          ].map(t => { const Icon = t.icon; return (
            <button key={t.id} onClick={() => setTab(t.id as any)} className={`flex-1 py-2 rounded-lg text-sm flex items-center justify-center gap-2 ${tab === t.id ? "bg-red-500" : "text-gray-400"}`}>
              <Icon className="w-4 h-4" /> {t.name}
            </button>
          );})}
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-red-500 border-t-transparent rounded-full animate-spin"></div></div> :
        streams.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><Video className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">{tab === "live" ? "Hozircha jonli efir yo'q" : "Hech narsa topilmadi"}</p></div> :
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {streams.map((s: any) => (
            <div key={s.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden hover:border-red-500/50 transition group">
              <div className="h-40 bg-gradient-to-br from-red-500 via-pink-500 to-purple-500 relative">
                {s.thumbnail ? <img src={s.thumbnail} alt="" className="w-full h-full object-cover" /> : <div className="flex items-center justify-center h-full text-6xl">📹</div>}
                {tab === "live" && <div className="absolute top-3 left-3 px-2 py-0.5 bg-red-500 text-xs rounded-full font-bold flex items-center gap-1"><div className="w-2 h-2 bg-white rounded-full animate-pulse" /> LIVE</div>}
                {s.viewers !== undefined && <div className="absolute top-3 right-3 px-2 py-0.5 bg-black/50 backdrop-blur text-xs rounded-full flex items-center gap-1"><Eye className="w-3 h-3" />{s.viewers}</div>}
                <button onClick={() => join(s.id)} className="absolute inset-0 flex items-center justify-center bg-black/30 opacity-0 group-hover:opacity-100 transition">
                  <div className="w-16 h-16 rounded-full bg-white/90 backdrop-blur flex items-center justify-center"><Play className="w-8 h-8 text-black fill-current ml-1" /></div>
                </button>
              </div>
              <div className="p-4">
                <h3 className="font-bold mb-1 line-clamp-2">{s.title}</h3>
                {s.description && <p className="text-sm text-gray-400 line-clamp-1 mb-2">{s.description}</p>}
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-red-500 to-pink-500 flex items-center justify-center text-sm font-bold">{s.streamer?.full_name?.[0] || s.streamer?.username?.[0] || "S"}</div>
                  <div>
                    <div className="text-sm font-medium">{s.streamer?.full_name || s.streamer?.username || "Strimer"}</div>
                    {s.streamer?.is_verified && <div className="text-xs text-blue-400">✓ Verified</div>}
                  </div>
                </div>
                <div className="flex items-center gap-3 text-xs text-gray-400">
                  <span className="px-2 py-0.5 bg-red-500/20 text-red-300 rounded">{s.category}</span>
                  {s.scheduled_for && <span className="flex items-center gap-1"><Calendar className="w-3 h-3" />{new Date(s.scheduled_for).toLocaleString()}</span>}
                </div>
                <div className="flex gap-2 mt-3">
                  <button onClick={() => join(s.id)} className="flex-1 py-2 bg-gradient-to-r from-red-500 to-pink-500 rounded-lg text-sm font-medium">{tab === "live" ? "Ko'rish" : "Eslatma"}</button>
                  {tab === "live" && <button onClick={async () => {
                    const t = localStorage.getItem("token");
                    if (!t) return;
                    const amount = prompt("Donation miqdori (so'm):", "5000");
                    if (amount) await fetch(`${API_URL}/api/v1/streams/${s.id}/donate`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ amount: parseInt(amount), message: "Donate!" }) });
                  }} className="px-3 py-2 bg-yellow-500/20 text-yellow-400 rounded-lg text-sm"><Gift className="w-4 h-4" /></button>}
                </div>
              </div>
            </div>
          ))}
        </div>}
      </div>

      {showSchedule && <ScheduleForm onClose={() => setShowSchedule(false)} onCreated={load} />}
    </div>
  );
}

function ScheduleForm({ onClose, onCreated }: { onClose: () => void; onCreated: () => void }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("general");
  const [datetime, setDatetime] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    if (!title || !datetime) return;
    const t = localStorage.getItem("token");
    setLoading(true);
    await fetch(`${API_URL}/api/v1/streams/schedule`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ title, description, category, scheduled_for: new Date(datetime).toISOString() }) });
    setLoading(false); onCreated(); onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-md w-full" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">Efir rejalashtirish</h2>
          <button onClick={onClose}><X className="w-5 h-5" /></button>
        </div>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Efir sarlavhasi" className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3" />
        <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} placeholder="Tavsif" className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3" />
        <select value={category} onChange={(e) => setCategory(e.target.value)} className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3">
          <option value="general">Umumiy</option>
          <option value="startup">Startap</option>
          <option value="tech">Texnologiya</option>
          <option value="education">Ta'lim</option>
          <option value="gaming">O'yin</option>
        </select>
        <input type="datetime-local" value={datetime} onChange={(e) => setDatetime(e.target.value)} className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3" />
        <button onClick={submit} disabled={loading} className="w-full py-3 bg-gradient-to-r from-red-500 to-pink-500 rounded-xl font-bold disabled:opacity-50">{loading ? "Yaratilmoqda..." : "Rejalashtirish"}</button>
      </div>
    </div>
  );
}
