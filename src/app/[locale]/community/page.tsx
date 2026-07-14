"use client";
import { useState, useEffect } from "react";
import { Users, Plus, Search, MessageCircle, Vote, Calendar, TrendingUp, X, Check, BarChart3, Send } from "lucide-react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function CommunityPage() {
  const [tab, setTab] = useState<"communities" | "events" | "polls" | "quizzes">("communities");
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [showCreate, setShowCreate] = useState(false);

  useEffect(() => { load(); }, [tab]);

  const load = async () => {
    setLoading(true);
    let url = "";
    if (tab === "communities") url = "/social/communities";
    else if (tab === "events") url = "/social/events";
    else if (tab === "polls") url = "/polls/active";
    else if (tab === "quizzes") url = "/education/quizzes";
    try { const r = await fetch(`${API_URL}/api/v1${url}`); if (r.ok) setData(await r.json()); } catch {}
    setLoading(false);
  };

  const joinCommunity = async (id: number) => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    await fetch(`${API_URL}/api/v1/social/communities/${id}/join`, { method: "POST", headers: { Authorization: `Bearer ${t}` } });
    load();
  };

  const rsvpEvent = async (id: number) => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    await fetch(`${API_URL}/api/v1/social/events/${id}/rsvp`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ status: "going" }) });
    alert("✅ Qabul qilindi!");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-teal-900 to-slate-900 text-white p-4 md:p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
          <div>
            <h1 className="text-4xl font-bold flex items-center gap-3"><Users className="w-10 h-10 text-teal-400" /> Jamiyat</h1>
            <p className="text-gray-400 mt-1">Communities, tadbirlar, so'rovnomalar, viktorinalar</p>
          </div>
          <button onClick={() => setShowCreate(true)} className="px-5 py-2.5 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-xl font-medium flex items-center gap-2"><Plus className="w-4 h-4" /> Yaratish</button>
        </div>

        <div className="flex gap-2 mb-6 bg-white/5 p-1 rounded-xl overflow-x-auto">
          {[
            { id: "communities", name: "👥 Communities", icon: Users },
            { id: "events", name: "📅 Events", icon: Calendar },
            { id: "polls", name: "🗳 So'rovnomalar", icon: Vote },
            { id: "quizzes", name: "❓ Viktorinalar", icon: BarChart3 },
          ].map(t => { const Icon = t.icon; return (
            <button key={t.id} onClick={() => setTab(t.id as any)} className={`flex-shrink-0 px-4 py-2 rounded-lg text-sm flex items-center gap-2 ${tab === t.id ? "bg-teal-500" : "text-gray-400"}`}>
              <Icon className="w-4 h-4" /> {t.name}
            </button>
          );})}
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Qidirish..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-teal-500 focus:outline-none" />
          </div>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-teal-500 border-t-transparent rounded-full animate-spin"></div></div> :
        data.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><Users className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">Hech narsa topilmadi</p></div> :
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {tab === "communities" && data.map((c: any) => (
            <div key={c.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 hover:border-teal-500/50 transition">
              <div className="flex items-start gap-3 mb-3">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-teal-500 to-cyan-500 flex items-center justify-center text-2xl font-bold">{c.name[0]}</div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-bold truncate">{c.name}</h3>
                  <div className="text-xs text-gray-400">{c.members_count} a'zo</div>
                </div>
              </div>
              <p className="text-sm text-gray-300 line-clamp-2 mb-3">{c.description}</p>
              <div className="flex items-center gap-2 text-xs text-gray-400 mb-3">
                <span className="px-2 py-0.5 bg-teal-500/20 text-teal-300 rounded">{c.category}</span>
              </div>
              <button onClick={() => joinCommunity(c.id)} className="w-full py-2 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-lg text-sm font-medium">Qo'shilish</button>
            </div>
          ))}

          {tab === "events" && data.map((e: any) => (
            <div key={e.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden hover:border-teal-500/50 transition">
              <div className="h-32 bg-gradient-to-br from-teal-500 to-blue-500 relative">
                {e.cover_image ? <img src={e.cover_image} alt="" className="w-full h-full object-cover" /> : <div className="flex items-center justify-center h-full text-5xl">📅</div>}
                {e.is_online && <div className="absolute top-2 right-2 px-2 py-0.5 bg-green-500 text-xs rounded-full">Online</div>}
                {!e.is_free && <div className="absolute top-2 left-2 px-2 py-0.5 bg-yellow-500 text-black text-xs rounded-full font-bold">{e.price.toLocaleString()} so'm</div>}
              </div>
              <div className="p-4">
                <h3 className="font-bold mb-1 line-clamp-2">{e.title}</h3>
                <p className="text-xs text-gray-400 mb-2 line-clamp-2">{e.description}</p>
                <div className="text-xs text-gray-300 mb-3">
                  📅 {new Date(e.start_at).toLocaleString()}<br />
                  👥 {e.attendees_count} ishtirokchi<br />
                  {e.location && <>📍 {e.location}</>}
                </div>
                <button onClick={() => rsvpEvent(e.id)} className="w-full py-2 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-lg text-sm font-medium">Boraman</button>
              </div>
            </div>
          ))}

          {tab === "polls" && data.map((p: any) => (
            <div key={p.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5">
              <div className="flex items-center gap-2 mb-3">
                <Vote className="w-5 h-5 text-teal-400" />
                <span className="text-xs text-gray-400">So'rovnoma</span>
              </div>
              <h3 className="font-bold mb-3">{p.question}</h3>
              {p.options?.map((o: any) => (
                <button key={o.id} onClick={async () => {
                  const t = localStorage.getItem("token");
                  if (!t) return alert("Avval kiring");
                  await fetch(`${API_URL}/api/v1/social/polls/${p.id}/vote`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ option_ids: [o.id] }) });
                  load();
                }} className="w-full mb-2 p-2 bg-white/5 hover:bg-white/10 rounded-lg text-left relative overflow-hidden">
                  <div className="absolute inset-y-0 left-0 bg-teal-500/30" style={{ width: `${o.percent || 0}%` }}></div>
                  <div className="relative flex items-center justify-between">
                    <span>{o.text}</span>
                    <span className="text-sm text-gray-400">{o.percent?.toFixed(0) || 0}%</span>
                  </div>
                </button>
              ))}
            </div>
          ))}

          {tab === "quizzes" && data.map((q: any) => (
            <Link href={`/quiz/${q.id}`} key={q.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 hover:border-teal-500/50 transition">
              <div className="flex items-center gap-2 mb-3">
                <BarChart3 className="w-5 h-5 text-teal-400" />
                <span className="text-xs px-2 py-0.5 bg-teal-500/20 text-teal-300 rounded">{q.difficulty}</span>
              </div>
              <h3 className="font-bold mb-2">{q.title}</h3>
              <p className="text-sm text-gray-400 line-clamp-2 mb-3">{q.description}</p>
              <div className="flex items-center gap-3 text-xs text-gray-400">
                <span>❓ {q.questions_count} savol</span>
                <span>🎯 {q.attempts_count} urinish</span>
              </div>
            </Link>
          ))}
        </div>}
      </div>

      {showCreate && <CreateModal type={tab} onClose={() => setShowCreate(false)} onCreated={load} />}
    </div>
  );
}

function CreateModal({ type, onClose, onCreated }: { type: string; onClose: () => void; onCreated: () => void }) {
  const [data, setData] = useState<any>({});
  const t = localStorage.getItem("token");

  const submit = async () => {
    let url = "";
    if (type === "communities") url = "/social/communities";
    else if (type === "events") url = "/social/events";
    else if (type === "polls") url = "/social/polls";
    
    await fetch(`${API_URL}/api/v1${url}`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify(data) });
    onCreated(); onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-md w-full" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold capitalize">Yangi {type}</h2>
          <button onClick={onClose}><X className="w-5 h-5" /></button>
        </div>
        <input onChange={(e) => setData({ ...data, name: e.target.value })} placeholder="Nomi" className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3" />
        <textarea onChange={(e) => setData({ ...data, description: e.target.value })} rows={3} placeholder="Tavsif" className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3" />
        {type === "polls" && <input onChange={(e) => setData({ ...data, question: e.target.value, options: e.target.value.split(",").map(s => s.trim()) })} placeholder="Savol va variantlar (vergul bilan)" className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3" />}
        <button onClick={submit} className="w-full py-3 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-xl font-bold">Yaratish</button>
      </div>
    </div>
  );
}
