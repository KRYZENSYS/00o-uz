"use client";
import { useState, useEffect } from "react";
import { BarChart3, Users, Rocket, Briefcase, Wrench, DollarSign, Activity, Shield, Send, Megaphone, Bell, Database, AlertTriangle, Check, X, Eye, Edit, Trash2, Search } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function AdminPage() {
  const [tab, setTab] = useState("dashboard");
  const [users, setUsers] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [reports, setReports] = useState<any[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => { if (tab === "users") loadUsers(); if (tab === "dashboard") loadStats(); if (tab === "moderation") loadReports(); }, [tab]);

  const loadStats = async () => {
    const t = localStorage.getItem("token");
    try { const r = await fetch(`${API_URL}/api/v1/admin/dashboard`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setStats(await r.json()); } catch {}
  };

  const loadUsers = async () => {
    const t = localStorage.getItem("token");
    try { const r = await fetch(`${API_URL}/api/v1/admin/users?search=${search}`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setUsers(await r.json()); } catch {}
  };

  const loadReports = async () => {
    const t = localStorage.getItem("token");
    try { const r = await fetch(`${API_URL}/api/v1/admin/reports?status=pending`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setReports(await r.json()); } catch {}
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-red-900 to-slate-900 text-white p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-3 mb-6">
          <Shield className="w-10 h-10 text-red-400" />
          <div>
            <h1 className="text-3xl font-bold">Admin Panel</h1>
            <p className="text-gray-400 text-sm">Boshqaruv va monitoring</p>
          </div>
        </div>

        <div className="flex gap-2 mb-6 overflow-x-auto bg-white/5 p-1 rounded-xl">
          {[
            { id: "dashboard", name: "Dashboard", icon: BarChart3 },
            { id: "users", name: "Foydalanuvchilar", icon: Users },
            { id: "moderation", name: "Moderatsiya", icon: AlertTriangle },
            { id: "broadcast", name: "Xabar yuborish", icon: Megaphone },
            { id: "push", name: "Push", icon: Bell },
            { id: "settings", name: "Sozlamalar", icon: Edit },
            { id: "logs", name: "Loglar", icon: Database },
          ].map(t => { const Icon = t.icon; return (
            <button key={t.id} onClick={() => setTab(t.id)} className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap flex items-center gap-2 ${tab === t.id ? "bg-red-500" : "text-gray-400"}`}>
              <Icon className="w-4 h-4" /> {t.name}
            </button>
          );})}
        </div>

        {tab === "dashboard" && stats && (
          <div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              {[
                { l: "Foydalanuvchilar", v: stats.users_total, icon: Users, c: "from-blue-500 to-cyan-500" },
                { l: "Startaplar", v: stats.startups_total, icon: Rocket, c: "from-purple-500 to-pink-500" },
                { l: "Ish o'rinlari", v: stats.jobs_total, icon: Briefcase, c: "from-green-500 to-emerald-500" },
                { l: "Xizmatlar", v: stats.services_total, icon: Wrench, c: "from-yellow-500 to-orange-500" },
                { l: "Daromad", v: `${(stats.revenue_total || 0).toLocaleString()} so'm`, icon: DollarSign, c: "from-emerald-500 to-green-500" },
                { l: "Bugun faol", v: stats.active_today, icon: Activity, c: "from-rose-500 to-pink-500" },
                { l: "AI so'rovlar", v: stats.ai_requests_total, icon: BarChart3, c: "from-violet-500 to-purple-500" },
                { l: "Premium", v: stats.premium_count, icon: Shield, c: "from-yellow-400 to-orange-500" },
              ].map((s, i) => { const Icon = s.icon; return (
                <div key={i} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4">
                  <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${s.c} flex items-center justify-center mb-2`}><Icon className="w-5 h-5" /></div>
                  <div className="text-2xl font-bold">{s.v}</div>
                  <div className="text-xs text-gray-400">{s.l}</div>
                </div>
              );})}
            </div>
          </div>
        )}

        {tab === "users" && (
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4">
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && loadUsers()} placeholder="Foydalanuvchi qidirish..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl" />
            </div>
            <table className="w-full text-sm">
              <thead className="text-left text-gray-400 border-b border-white/10">
                <tr><th className="py-2">Foydalanuvchi</th><th>Email</th><th>Token</th><th>Status</th><th>Amal</th></tr>
              </thead>
              <tbody>
                {users.map((u: any) => (
                  <tr key={u.id} className="border-b border-white/5">
                    <td className="py-3 flex items-center gap-2">
                      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center text-xs font-bold">{u.full_name?.[0]}</div>
                      {u.full_name} @{u.username}
                    </td>
                    <td>{u.email}</td>
                    <td>{u.tokens}</td>
                    <td>{u.is_banned ? <span className="text-red-400">🚫 Ban</span> : u.is_active ? <span className="text-green-400">✅ Active</span> : <span className="text-gray-400">Inactive</span>}</td>
                    <td>
                      <button className="p-1 hover:bg-white/10 rounded mr-1"><Eye className="w-4 h-4" /></button>
                      <button className="p-1 hover:bg-white/10 rounded mr-1"><Edit className="w-4 h-4" /></button>
                      <button className="p-1 hover:bg-white/10 rounded text-red-400"><Trash2 className="w-4 h-4" /></button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {tab === "moderation" && (
          <div className="space-y-3">
            {reports.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><Check className="w-16 h-16 mx-auto text-green-400 mb-4" /><p className="text-gray-400">Yangi shikoyatlar yo'q</p></div> :
              reports.map((r: any) => (
                <div key={r.id} className="bg-white/5 border border-white/10 rounded-2xl p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-bold">{r.reporter?.full_name} → {r.reported?.full_name}</div>
                      <div className="text-sm text-gray-400">{r.reason} • {r.description}</div>
                    </div>
                    <div className="flex gap-2">
                      <button className="px-3 py-1 bg-green-500 rounded-lg text-sm flex items-center gap-1"><Check className="w-3 h-3" /> Rad etish</button>
                      <button className="px-3 py-1 bg-red-500 rounded-lg text-sm flex items-center gap-1"><X className="w-3 h-3" /> Bloklash</button>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        )}

        {tab === "broadcast" && <BroadcastForm />}
        {tab === "push" && <PushForm />}
      </div>
    </div>
  );
}

function BroadcastForm() {
  const [text, setText] = useState("");
  const [segment, setSegment] = useState("all");
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);

  const send = async () => {
    const t = localStorage.getItem("token");
    setLoading(true);
    await fetch(`${API_URL}/api/v1/admin/broadcast`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ text, segment }) });
    setLoading(false); setDone(true); setText("");
  };

  return (
    <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 max-w-xl">
      <h2 className="text-xl font-bold mb-4">📢 Xabar yuborish</h2>
      <select value={segment} onChange={(e) => setSegment(e.target.value)} className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3">
        <option value="all">Hammaga</option>
        <option value="premium">Premium foydalanuvchilar</option>
        <option value="free">Bepul foydalanuvchilar</option>
        <option value="active">Faol (24 soat ichida kirgan)</option>
        <option value="inactive">Nofaol (30 kun)</option>
      </select>
      <textarea value={text} onChange={(e) => setText(e.target.value)} rows={6} placeholder="Xabar matni..." className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3" />
      {done && <div className="text-green-400 text-sm mb-3">✅ Yuborildi!</div>}
      <button onClick={send} disabled={loading || !text.trim()} className="w-full py-3 bg-gradient-to-r from-red-500 to-pink-500 rounded-xl font-bold disabled:opacity-50">{loading ? "Yuborilmoqda..." : "Yuborish"}</button>
    </div>
  );
}

function PushForm() {
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [sent, setSent] = useState(false);

  const send = async () => {
    const t = localStorage.getItem("token");
    await fetch(`${API_URL}/api/v1/marketing/push/send`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ title, body, target_users: "all" }) });
    setSent(true); setTitle(""); setBody("");
  };

  return (
    <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 max-w-xl">
      <h2 className="text-xl font-bold mb-4 flex items-center gap-2"><Bell className="w-5 h-5" /> Push bildirishnoma</h2>
      <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Sarlavha" className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3" />
      <textarea value={body} onChange={(e) => setBody(e.target.value)} rows={4} placeholder="Matn..." className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3" />
      {sent && <div className="text-green-400 text-sm mb-3">✅ Yuborildi!</div>}
      <button onClick={send} disabled={!title || !body} className="w-full py-3 bg-gradient-to-r from-red-500 to-pink-500 rounded-xl font-bold disabled:opacity-50"><Send className="w-4 h-4 inline mr-1" /> Yuborish</button>
    </div>
  );
}
