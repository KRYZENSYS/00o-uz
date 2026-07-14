"use client";
import { useState, useEffect } from "react";
import { MessageSquare, Send, Phone, Video, PhoneIncoming, PhoneOutgoing, PhoneMissed, Search } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function CallsPage() {
  const [tab, setTab] = useState<"recent" | "contacts" | "keypad">("recent");
  const [history, setHistory] = useState<any[]>([]);
  const [contacts] = useState([
    { id: 1, name: "Aziz Karimov", avatar: "👨", online: true, lastCall: "5 min" },
    { id: 2, name: "Malika Yusupova", avatar: "👩", online: true, lastCall: "1 soat" },
    { id: 3, name: "Bobur Aliyev", avatar: "👨", online: false, lastCall: "2 kun" },
    { id: 4, name: "Nilufar Saidova", avatar: "👩", online: true, lastCall: "1 hafta" },
    { id: 5, name: "Sherzod Toshmatov", avatar: "👨", online: false, lastCall: "1 oy" },
  ]);
  const [search, setSearch] = useState("");

  useEffect(() => { load(); }, []);

  const load = async () => {
    const t = localStorage.getItem("token");
    try { const r = await fetch(`${API_URL}/api/v1/calls/history`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setHistory(await r.json()); } catch {}
  };

  const startCall = async (type: "audio" | "video", userId: number) => {
    const t = localStorage.getItem("token");
    const r = await fetch(`${API_URL}/api/v1/calls/start`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ callee_id: userId, call_type: type }) });
    if (r.ok) {
      const d = await r.json();
      alert(`📞 ${type === "video" ? "Video" : "Audio"} qo'ng'iroq boshlanmoqda...\nRoom: ${d.room_id}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-green-900 to-slate-900 text-white p-4 md:p-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 flex items-center gap-3"><Phone className="w-8 h-8 text-green-400" /> Qo'ng'iroqlar</h1>

        <div className="flex gap-2 mb-4 bg-white/5 p-1 rounded-xl">
          {[
            { id: "recent", name: "So'nggi" },
            { id: "contacts", name: "Kontaktlar" },
            { id: "keypad", name: "Klaviatura" },
          ].map(t => (
            <button key={t.id} onClick={() => setTab(t.id as any)} className={`flex-1 py-2 rounded-lg text-sm ${tab === t.id ? "bg-green-500" : "text-gray-400"}`}>{t.name}</button>
          ))}
        </div>

        {tab === "recent" && (
          <div className="space-y-2">
            {history.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><Phone className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">Qo'ng'iroqlar tarixchasi bo'sh</p></div> :
              history.map(c => (
                <div key={c.id} className="flex items-center gap-3 p-3 bg-white/5 rounded-xl">
                  {c.status === "missed" ? <PhoneMissed className="w-5 h-5 text-red-400" /> : c.status === "outgoing" ? <PhoneOutgoing className="w-5 h-5 text-blue-400" /> : <PhoneIncoming className="w-5 h-5 text-green-400" />}
                  <div className="flex-1">
                    <div className="font-medium">Qo'ng'iroq #{c.id}</div>
                    <div className="text-xs text-gray-400">{c.type} • {c.duration?.toFixed(0) || 0}s • {new Date(c.created_at).toLocaleString()}</div>
                  </div>
                </div>
              ))}
          </div>
        )}

        {tab === "contacts" && (
          <div>
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Kontakt qidirish..." className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-full" />
            </div>
            <div className="space-y-2">
              {contacts.filter(c => c.name.toLowerCase().includes(search.toLowerCase())).map(c => (
                <div key={c.id} className="flex items-center gap-3 p-3 bg-white/5 rounded-xl">
                  <div className="relative">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center text-2xl">{c.avatar}</div>
                    {c.online && <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-slate-900"></div>}
                  </div>
                  <div className="flex-1">
                    <div className="font-medium">{c.name}</div>
                    <div className="text-xs text-gray-400">{c.online ? "Online" : `Oxirgi: ${c.lastCall}`}</div>
                  </div>
                  <button onClick={() => startCall("audio", c.id)} className="p-2 bg-blue-500/20 text-blue-400 rounded-lg"><Phone className="w-4 h-4" /></button>
                  <button onClick={() => startCall("video", c.id)} className="p-2 bg-purple-500/20 text-purple-400 rounded-lg"><Video className="w-4 h-4" /></button>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab === "keypad" && <Keypad />}
      </div>
    </div>
  );
}

function Keypad() {
  const [num, setNum] = useState("");
  const keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"];

  return (
    <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 max-w-sm mx-auto">
      <div className="bg-white/5 rounded-xl p-4 mb-4 text-center text-2xl font-mono min-h-[3rem]">{num || "+998 "}</div>
      <div className="grid grid-cols-3 gap-3 mb-4">
        {keys.map(k => (
          <button key={k} onClick={() => setNum(n => n + k)} className="aspect-square bg-white/5 hover:bg-white/10 rounded-full text-2xl font-bold">{k}</button>
        ))}
      </div>
      <div className="flex gap-3">
        <button onClick={() => setNum(n => n.slice(0, -1))} className="flex-1 py-3 bg-white/5 rounded-xl">⌫ O'chirish</button>
        <button onClick={() => alert(`Qo'ng'iroq: ${num}`)} className="flex-1 py-3 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl font-bold flex items-center justify-center gap-2"><Phone className="w-5 h-5" /> Qo'ng'iroq</button>
      </div>
    </div>
  );
}
