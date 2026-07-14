"use client";
import { useState, useEffect } from "react";
import { Users, Rocket, Briefcase, DollarSign, MessageSquare, TrendingUp, Ban, Star, BarChart3, Settings, Send, Shield, Activity } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function AdminPage() {
  const [stats, setStats] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [tab, setTab] = useState("overview");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const headers = { Authorization: `Bearer ${localStorage.getItem("token")}` };
    fetch(`${API_URL}/api/v1/admin/stats/overview`, { headers }).then(r => r.ok && r.json().then(setStats));
    fetch(`${API_URL}/api/v1/admin/users`, { headers }).then(r => r.ok && r.json().then(setUsers));
    setLoading(false);
  }, []);

  const ban = async (id: number) => fetch(`${API_URL}/api/v1/admin/users/${id}/ban?reason=Admin`, { method: "POST", headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }}).then(() => location.reload());
  const premium = async (id: number) => fetch(`${API_URL}/api/v1/admin/users/${id}/premium?days=30`, { method: "POST", headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }}).then(() => location.reload());

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white"><div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div></div>;

  return (
    <div className="min-h-screen bg-slate-900 text-white p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 flex items-center gap-3"><Shield className="w-8 h-8 text-red-400" /> Admin Panel</h1>

        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {[{ id: "overview", label: "Umumiy", icon: BarChart3 }, { id: "users", label: "Users", icon: Users }, { id: "broadcast", label: "Xabarlar", icon: Send }, { id: "settings", label: "Sozlamalar", icon: Settings }].map(t => {
            const Icon = t.icon;
            return <button key={t.id} onClick={() => setTab(t.id)} className={`px-4 py-2 rounded-xl flex items-center gap-2 whitespace-nowrap ${tab === t.id ? "bg-purple-600" : "bg-white/5"}`}><Icon className="w-4 h-4" />{t.label}</button>;
          })}
        </div>

        {tab === "overview" && stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { l: "Foydalanuvchilar", v: stats.users, i: Users, c: "from-blue-500 to-cyan-500" },
              { l: "Startaplar", v: stats.startups, i: Rocket, c: "from-purple-500 to-pink-500" },
              { l: "Xizmatlar", v: stats.services, i: Briefcase, c: "from-green-500 to-emerald-500" },
              { l: "Ishlar", v: stats.jobs, i: Briefcase, c: "from-yellow-500 to-orange-500" },
              { l: "Xabarlar", v: stats.messages, i: MessageSquare, c: "from-pink-500 to-rose-500" },
              { l: "Daromad", v: `$${(stats.revenue/1000).toFixed(1)}K`, i: DollarSign, c: "from-emerald-500 to-green-500" },
              { l: "Bugun yangi", v: stats.new_users_today, i: TrendingUp, c: "from-indigo-500 to-purple-500" },
              { l: "Onlayn", v: 0, i: Activity, c: "from-teal-500 to-cyan-500" },
            ].map((c, i) => { const Icon = c.i; return (
              <div key={i} className={`p-5 rounded-2xl bg-gradient-to-br ${c.c}`}><Icon className="w-6 h-6 mb-2 opacity-80" /><div className="text-sm opacity-80">{c.l}</div><div className="text-3xl font-bold">{c.v}</div></div>
            );})}
          </div>
        )}

        {tab === "users" && (
          <div className="bg-white/5 rounded-2xl overflow-x-auto">
            <table className="w-full">
              <thead className="bg-white/5"><tr><th className="p-3 text-left">ID</th><th className="p-3 text-left">Email</th><th className="p-3 text-left">Username</th><th className="p-3 text-left">Role</th><th className="p-3 text-left">Status</th><th className="p-3 text-left">Premium</th><th className="p-3 text-left">Amallar</th></tr></thead>
              <tbody>{users.map(u => (
                <tr key={u.id} className="border-t border-white/10">
                  <td className="p-3">{u.id}</td><td className="p-3">{u.email}</td><td className="p-3">@{u.username}</td>
                  <td className="p-3"><span className="px-2 py-1 bg-purple-500/20 rounded text-xs">{u.role}</span></td>
                  <td className="p-3">{u.is_active ? "✅" : "🚫"}</td><td className="p-3">{u.is_premium ? "💎" : "—"}</td>
                  <td className="p-3 flex gap-2">
                    <button onClick={() => premium(u.id)} className="p-1.5 bg-yellow-500/20 rounded"><Star className="w-4 h-4" /></button>
                    <button onClick={() => ban(u.id)} className="p-1.5 bg-red-500/20 rounded"><Ban className="w-4 h-4" /></button>
                  </td>
                </tr>
              ))}</tbody>
            </table>
          </div>
        )}

        {tab === "broadcast" && (
          <div className="bg-white/5 rounded-2xl p-6 max-w-2xl">
            <h2 className="text-xl font-bold mb-4">📤 Barchaga xabar</h2>
            <input placeholder="Sarlavha" className="w-full p-3 bg-white/5 border border-white/10 rounded-xl mb-3" />
            <textarea placeholder="Xabar" rows={5} className="w-full p-3 bg-white/5 border border-white/10 rounded-xl mb-3" />
            <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl font-bold">Yuborish</button>
          </div>
        )}

        {tab === "settings" && (
          <div className="bg-white/5 rounded-2xl p-6 max-w-2xl">
            <h2 className="text-xl font-bold mb-4">⚙️ AI Sozlamalari</h2>
            <label className="text-sm text-gray-400">Model</label>
            <select className="w-full p-3 bg-white/5 border border-white/10 rounded-xl mb-3">
              <option>llama-3.3-70b-versatile</option><option>llama-3.1-8b-instant</option><option>mixtral-8x7b-32768</option>
            </select>
            <button className="px-6 py-3 bg-purple-600 rounded-xl">Saqlash</button>
          </div>
        )}
      </div>
    </div>
  );
}
