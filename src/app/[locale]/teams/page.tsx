"use client";
import { useState, useEffect } from "react";
import { Users, Search, UserPlus, MapPin, Star, MessageSquare, Crown, Code, Palette, Megaphone } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function TeamsPage() {
  const [teams, setTeams] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [role, setRole] = useState("");

  useEffect(() => { load(); }, [role]);

  const load = async () => {
    setLoading(true);
    const p = new URLSearchParams();
    if (search) p.append("search", search);
    if (role) p.append("role", role);
    try { const r = await fetch(`${API_URL}/api/v1/teams/?${p}`); setTeams(await r.json()); } catch {}
    setLoading(false);
  };

  const join = async (id: number) => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    const r = await fetch(`${API_URL}/api/v1/teams/${id}/join`, { method: "POST", headers: { Authorization: `Bearer ${t}` } });
    if (r.ok) alert("Ariza yuborildi!");
  };

  const roleIcon = (r: string) => {
    const map: any = { developer: Code, designer: Palette, marketer: Megaphone, cofounder: Crown };
    return map[r] || Users;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-cyan-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold flex items-center gap-3"><Users className="w-10 h-10 text-cyan-400" /> Jamoalar</h1>
          <p className="text-gray-400 mt-2">Hamkasblar va co-founder toping</p>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6 flex flex-wrap gap-3">
          <div className="flex-1 min-w-[200px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && load()}
              placeholder="Jamoa qidirish..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-cyan-500 focus:outline-none" />
          </div>
          <select value={role} onChange={(e) => setRole(e.target.value)} className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
            <option value="">Barcha rollar</option>
            <option value="cofounder">Co-founder</option>
            <option value="developer">Dasturchi</option>
            <option value="designer">Dizayner</option>
            <option value="marketer">Marketolog</option>
          </select>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin"></div></div> :
        teams.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><Users className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">Jamoalar topilmadi</p></div> :
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {teams.map(t => (
            <div key={t.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 hover:border-cyan-500/50 transition">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center text-2xl font-bold">{t.name[0]}</div>
                  <div>
                    <h3 className="font-bold text-lg">{t.name}</h3>
                    <div className="text-xs text-gray-400">{t.members_count} a'zo</div>
                  </div>
                </div>
                {t.is_featured && <span className="px-2 py-0.5 bg-yellow-500/20 text-yellow-400 text-xs rounded-full">⭐ Top</span>}
              </div>
              <p className="text-gray-300 text-sm mb-3 line-clamp-2">{t.description}</p>
              {t.looking_for?.length > 0 && (
                <div className="mb-3">
                  <div className="text-xs text-gray-400 mb-1">Qidirilmoqda:</div>
                  <div className="flex flex-wrap gap-2">{t.looking_for.map((r: string) => { const Icon = roleIcon(r); return (
                    <span key={r} className="px-2 py-1 bg-cyan-500/20 text-cyan-300 rounded-lg text-xs flex items-center gap-1"><Icon className="w-3 h-3" />{r}</span>
                  );})}</div>
                </div>
              )}
              {t.skills_needed?.length > 0 && (
                <div className="mb-3">
                  <div className="text-xs text-gray-400 mb-1">Ko'nikmalar:</div>
                  <div className="flex flex-wrap gap-1">{t.skills_needed.slice(0, 5).map((s: string) => <span key={s} className="px-2 py-0.5 bg-white/5 text-xs rounded text-gray-300">{s}</span>)}</div>
                </div>
              )}
              <button onClick={() => join(t.id)} className="w-full mt-3 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl font-medium text-sm flex items-center justify-center gap-1">
                <UserPlus className="w-4 h-4" /> Qo'shilish
              </button>
            </div>
          ))}
        </div>}
      </div>
    </div>
  );
}
