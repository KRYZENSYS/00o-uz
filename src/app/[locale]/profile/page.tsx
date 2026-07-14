"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { User, Mail, Phone, Edit, Camera, Sparkles, Heart, Briefcase, Rocket, Settings, LogOut, Crown, Award, Bell } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ProfilePage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [editing, setEditing] = useState(false);
  const [form, setForm] = useState({ full_name: "", bio: "", phone: "" });

  useEffect(() => {
    const t = localStorage.getItem("token");
    if (!t) return router.push("/");
    fetch(`${API_URL}/api/v1/auth/me`, { headers: { Authorization: `Bearer ${t}` }})
      .then(r => r.ok ? r.json() : null)
      .then(d => { if (d) { setUser(d); setForm({ full_name: d.full_name, bio: d.bio || "", phone: d.phone || "" }); } });
  }, []);

  if (!user) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white"><div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div></div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-5xl mx-auto">
        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl overflow-hidden mb-6">
          <div className="h-40 bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 relative">
            <button className="absolute top-3 right-3 p-2 bg-black/30 hover:bg-black/50 rounded-lg"><Camera className="w-5 h-5" /></button>
          </div>
          <div className="px-6 pb-6 -mt-16">
            <div className="flex items-end justify-between flex-wrap gap-4">
              <div className="flex items-end gap-4">
                <div className="w-28 h-28 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 border-4 border-slate-900 flex items-center justify-center text-4xl font-bold">
                  {user.full_name?.[0] || user.username?.[0] || "U"}
                </div>
                <div className="pb-2">
                  <h1 className="text-2xl font-bold flex items-center gap-2">
                    {user.full_name}
                    {user.is_verified && <span className="text-blue-400">✓</span>}
                    {user.is_premium && <Crown className="w-5 h-5 text-yellow-400" />}
                  </h1>
                  <p className="text-gray-400">@{user.username}</p>
                  <p className="text-sm text-gray-500 mt-1">{user.bio || "Bio qo'shilmagan"}</p>
                </div>
              </div>
              <div className="flex gap-2">
                <button onClick={() => setEditing(!editing)} className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-xl flex items-center gap-2 text-sm">
                  <Edit className="w-4 h-4" /> Tahrirlash
                </button>
                {!user.is_premium && (
                  <button className="px-4 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-black rounded-xl flex items-center gap-2 text-sm font-bold">
                    <Crown className="w-4 h-4" /> Premium
                  </button>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-6">
              {[
                { l: "Token", v: user.tokens || 0, icon: Sparkles, c: "from-purple-500 to-pink-500" },
                { l: "Premium", v: user.is_premium ? "Ha" : "Yo'q", icon: Crown, c: "from-yellow-500 to-orange-500" },
                { l: "Verified", v: user.is_verified ? "✓" : "—", icon: Award, c: "from-blue-500 to-cyan-500" },
                { l: "Role", v: user.role, icon: User, c: "from-green-500 to-emerald-500" }
              ].map((s, i) => { const Icon = s.icon; return (
                <div key={i} className={`p-3 rounded-xl bg-gradient-to-br ${s.c} bg-opacity-20 border border-white/10`}>
                  <Icon className="w-5 h-5 mb-1 opacity-80" />
                  <div className="text-xs opacity-80">{s.l}</div>
                  <div className="text-lg font-bold">{s.v}</div>
                </div>
              );})}
            </div>
          </div>
        </div>

        {editing && (
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 mb-6">
            <h2 className="text-xl font-bold mb-4">Tahrirlash</h2>
            <div className="space-y-3">
              <div><label className="text-sm text-gray-400">To'liq ism</label>
                <input value={form.full_name} onChange={(e) => setForm({...form, full_name: e.target.value})} className="w-full mt-1 px-4 py-3 bg-white/5 border border-white/10 rounded-xl" /></div>
              <div><label className="text-sm text-gray-400">Telefon</label>
                <input value={form.phone} onChange={(e) => setForm({...form, phone: e.target.value})} className="w-full mt-1 px-4 py-3 bg-white/5 border border-white/10 rounded-xl" /></div>
              <div><label className="text-sm text-gray-400">Bio</label>
                <textarea value={form.bio} onChange={(e) => setForm({...form, bio: e.target.value})} rows={3} className="w-full mt-1 px-4 py-3 bg-white/5 border border-white/10 rounded-xl" /></div>
              <button onClick={() => setEditing(false)} className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl font-bold">Saqlash</button>
            </div>
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-4">
          {[
            { l: "Startaplarim", v: 0, icon: Rocket, c: "from-blue-500 to-cyan-500" },
            { l: "Xizmatlarim", v: 0, icon: Briefcase, c: "from-yellow-500 to-orange-500" },
            { l: "Sevimlilar", v: 0, icon: Heart, c: "from-pink-500 to-rose-500" },
            { l: "Bildirishnomalar", v: 0, icon: Bell, c: "from-green-500 to-emerald-500" }
          ].map((s, i) => { const Icon = s.icon; return (
            <div key={i} className={`p-5 rounded-2xl bg-gradient-to-br ${s.c} bg-opacity-10 border border-white/10 cursor-pointer hover:bg-opacity-20`}>
              <div className="flex items-center gap-3">
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${s.c} flex items-center justify-center`}><Icon className="w-6 h-6" /></div>
                <div><div className="text-sm text-gray-400">{s.l}</div><div className="text-2xl font-bold">{s.v}</div></div>
              </div>
            </div>
          );})}
        </div>
      </div>
    </div>
  );
}
