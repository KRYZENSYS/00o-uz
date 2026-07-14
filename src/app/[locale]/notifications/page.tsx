"use client";
import { useState, useEffect } from "react";
import { Bell, Heart, MessageCircle, UserPlus, DollarSign, Crown, Settings, Trash2, Check } from "lucide-react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function NotificationsPage() {
  const [notifs, setNotifs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "unread">("all");

  useEffect(() => { load(); }, [filter]);

  const load = async () => {
    const t = localStorage.getItem("token");
    if (!t) return setLoading(false);
    try {
      const r = await fetch(`${API_URL}/api/v1/notifications/?unread_only=${filter === "unread"}`, { headers: { Authorization: `Bearer ${t}` }});
      if (r.ok) setNotifs(await r.json());
    } catch {}
    setLoading(false);
  };

  const markRead = async (id: number) => {
    const t = localStorage.getItem("token");
    await fetch(`${API_URL}/api/v1/notifications/mark-read/${id}`, { method: "POST", headers: { Authorization: `Bearer ${t}` }});
    load();
  };

  const markAll = async () => {
    const t = localStorage.getItem("token");
    await fetch(`${API_URL}/api/v1/notifications/mark-all-read`, { method: "POST", headers: { Authorization: `Bearer ${t}` }});
    load();
  };

  const del = async (id: number) => {
    const t = localStorage.getItem("token");
    await fetch(`${API_URL}/api/v1/notifications/${id}`, { method: "DELETE", headers: { Authorization: `Bearer ${t}` }});
    load();
  };

  const icon = (type: string) => {
    const map: any = { like: Heart, comment: MessageCircle, follow: UserPlus, payment: DollarSign, premium: Crown, system: Settings };
    return map[type] || Bell;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-3xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold flex items-center gap-3"><Bell className="w-8 h-8 text-indigo-400" /> Bildirishnomalar</h1>
          <div className="flex gap-2">
            <button onClick={() => setFilter("all")} className={`px-3 py-1.5 rounded-lg text-sm ${filter === "all" ? "bg-indigo-600" : "bg-white/5"}`}>Hammasi</button>
            <button onClick={() => setFilter("unread")} className={`px-3 py-1.5 rounded-lg text-sm ${filter === "unread" ? "bg-indigo-600" : "bg-white/5"}`}>O'qilmagan</button>
            <button onClick={markAll} className="px-3 py-1.5 bg-green-500/20 text-green-400 rounded-lg text-sm flex items-center gap-1"><Check className="w-4 h-4" /> Hammasini o'qish</button>
          </div>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div></div> :
        notifs.length === 0 ? (
          <div className="text-center py-20 bg-white/5 rounded-2xl">
            <Bell className="w-16 h-16 mx-auto text-gray-600 mb-4" />
            <p className="text-gray-400">{filter === "unread" ? "O'qilmagan bildirishnomalar yo'q" : "Bildirishnomalar yo'q"}</p>
          </div>
        ) : (
          <div className="space-y-2">
            {notifs.map((n) => {
              const Icon = icon(n.type);
              return (
                <div key={n.id} className={`p-4 rounded-2xl border flex items-start gap-3 ${n.is_read ? "bg-white/5 border-white/10" : "bg-indigo-500/10 border-indigo-500/30"}`}>
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center flex-shrink-0">
                    <Icon className="w-5 h-5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-medium">{n.title}</div>
                    <p className="text-sm text-gray-400 mt-0.5">{n.message}</p>
                    <div className="text-xs text-gray-500 mt-1">{new Date(n.created_at).toLocaleString()}</div>
                  </div>
                  <div className="flex gap-1 flex-shrink-0">
                    {!n.is_read && <button onClick={() => markRead(n.id)} className="p-1.5 hover:bg-white/10 rounded-lg"><Check className="w-4 h-4" /></button>}
                    <button onClick={() => del(n.id)} className="p-1.5 hover:bg-red-500/20 text-red-400 rounded-lg"><Trash2 className="w-4 h-4" /></button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
