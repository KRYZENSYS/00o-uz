"use client";
import { useState, useEffect } from "react";
import { Trophy, Award, Star, Crown, Zap, Flame, TrendingUp, Target, Sparkles, BookOpen, Rocket, Briefcase, Wrench, Users, Eye, Heart } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ProfilePage({ params }: { params: { id: string } }) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<"overview" | "badges" | "missions" | "leaderboard">("overview");

  useEffect(() => { load(); }, []);

  const load = async () => {
    const t = localStorage.getItem("token");
    try { const r = await fetch(`${API_URL}/api/v1/game/me`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setData(await r.json()); } catch {}
    setLoading(false);
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white"><div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div></div>;
  if (!data) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">Ma'lumot yo'q</div>;

  const levelColors: any = { gray: "from-gray-500 to-gray-700", green: "from-green-500 to-emerald-700", blue: "from-blue-500 to-cyan-700", purple: "from-purple-500 to-pink-700", orange: "from-orange-500 to-red-700", red: "from-red-500 to-pink-700", yellow: "from-yellow-500 to-orange-700", pink: "from-pink-500 to-rose-700", cyan: "from-cyan-500 to-blue-700", rainbow: "from-pink-500 via-yellow-500 to-blue-500" };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-4 md:p-6">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6 mb-6">
          <div className="flex items-center gap-4 mb-4">
            <div className={`w-20 h-20 rounded-2xl bg-gradient-to-br ${levelColors[data.level.color]} flex items-center justify-center`}>
              <Trophy className="w-10 h-10" />
            </div>
            <div className="flex-1">
              <h1 className="text-2xl font-bold">Level {data.level.level}</h1>
              <p className="text-gray-400">{data.level.name}</p>
              <div className="mt-2">
                <div className="flex items-center justify-between text-xs mb-1">
                  <span>{data.xp} XP</span>
                  {data.next_level && <span>{data.next_level.xp_required} XP</span>}
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                  <div className={`h-full bg-gradient-to-r ${levelColors[data.level.color]} transition-all`} style={{ width: `${data.progress}%` }}></div>
                </div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-yellow-400">#{data.rank}</div>
              <div className="text-xs text-gray-400">global reyting</div>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-3 text-center">
            <div className="bg-white/5 rounded-xl p-3"><Flame className="w-5 h-5 mx-auto mb-1 text-orange-400" /><div className="font-bold">{data.streak_days}</div><div className="text-xs text-gray-400">streak</div></div>
            <div className="bg-white/5 rounded-xl p-3"><Award className="w-5 h-5 mx-auto mb-1 text-purple-400" /><div className="font-bold">{data.badges_total}</div><div className="text-xs text-gray-400">yutuq</div></div>
            <div className="bg-white/5 rounded-xl p-3"><Sparkles className="w-5 h-5 mx-auto mb-1 text-yellow-400" /><div className="font-bold">{data.xp}</div><div className="text-xs text-gray-400">XP</div></div>
          </div>
        </div>

        <div className="flex gap-2 mb-4 bg-white/5 p-1 rounded-xl">
          {["overview", "badges", "missions", "leaderboard"].map(t => (
            <button key={t} onClick={() => setTab(t as any)} className={`flex-1 py-2 rounded-lg text-sm capitalize ${tab === t ? "bg-purple-500" : "text-gray-400"}`}>{t === "leaderboard" ? "Top" : t === "missions" ? "Missiyalar" : t === "badges" ? "Yutuqlar" : "Umumiy"}</button>
          ))}
        </div>

        {tab === "overview" && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {data.badges.slice(0, 8).map((b: any) => (
              <div key={b.id} className="bg-white/5 border border-white/10 rounded-2xl p-4 text-center">
                <div className="text-4xl mb-2">{b.icon}</div>
                <div className="font-bold text-sm">{b.name}</div>
                <div className="text-xs text-gray-400 mt-1">+{b.xp} XP</div>
              </div>
            ))}
          </div>
        )}

        {tab === "badges" && (
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {data.badges.map((b: any) => (
              <div key={b.id} className="bg-white/5 border border-white/10 rounded-2xl p-4 text-center hover:border-yellow-500/50">
                <div className="text-5xl mb-2">{b.icon}</div>
                <div className="font-bold">{b.name}</div>
                <div className="text-xs text-gray-400 mt-1">{b.desc}</div>
                <div className="text-xs text-yellow-400 mt-2">+{b.xp} XP</div>
              </div>
            ))}
          </div>
        )}

        {tab === "missions" && <DailyMissions />}

        {tab === "leaderboard" && <Leaderboard />}
      </div>
    </div>
  );
}

function DailyMissions() {
  const [missions, setMissions] = useState<any[]>([]);
  useEffect(() => {
    const t = localStorage.getItem("token");
    fetch(`${API_URL}/api/v1/game/missions`, { headers: { Authorization: `Bearer ${t}` } }).then(r => r.ok ? r.json() : []).then(setMissions);
  }, []);

  return (
    <div className="space-y-3">
      {missions.map((m: any) => (
        <div key={m.id} className={`bg-white/5 border rounded-2xl p-4 ${m.completed ? "border-green-500/50" : "border-white/10"}`}>
          <div className="flex items-center justify-between mb-2">
            <div>
              <div className="font-bold">{m.name}</div>
              <div className="text-xs text-gray-400">{m.desc}</div>
            </div>
            <div className="text-yellow-400 font-bold">+{m.reward} XP</div>
          </div>
          <div className="h-2 bg-white/10 rounded-full overflow-hidden mb-2">
            <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500" style={{ width: `${(m.progress / m.target) * 100}%` }}></div>
          </div>
          <div className="flex items-center justify-between text-xs">
            <span className="text-gray-400">{m.progress}/{m.target}</span>
            {m.completed ? <span className="text-green-400">✅ Bajarildi</span> : <span className="text-gray-400">⏳ Kutilmoqda</span>}
          </div>
        </div>
      ))}
    </div>
  );
}

function Leaderboard() {
  const [data, setData] = useState<any[]>([]);
  useEffect(() => { fetch(`${API_URL}/api/v1/game/leaderboard`).then(r => r.ok ? r.json() : []).then(setData); }, []);

  return (
    <div className="space-y-2">
      {data.map((u: any) => (
        <div key={u.user.id} className={`flex items-center gap-3 p-3 rounded-xl ${u.rank <= 3 ? "bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-500/30" : "bg-white/5"}`}>
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center font-bold text-lg">{u.rank <= 3 ? ["🥇", "🥈", "🥉"][u.rank - 1] : u.rank}</div>
          <div className="flex-1">
            <div className="font-bold">{u.user.full_name}</div>
            <div className="text-xs text-gray-400">Level {u.level}</div>
          </div>
          <div className="font-bold text-yellow-400">{u.user.xp} XP</div>
        </div>
      ))}
    </div>
  );
}
