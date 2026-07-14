"use client";
import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { Search, Users, Rocket, Briefcase, Wrench, GraduationCap, TrendingUp, Filter } from "lucide-react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function SearchPage() {
  const params = useSearchParams();
  const initialQ = params.get("q") || "";
  const [q, setQ] = useState(initialQ);
  const [type, setType] = useState("all");
  const [results, setResults] = useState<any>({ users: [], startups: [], jobs: [], services: [], courses: [], investors: [], total: 0 });
  const [loading, setLoading] = useState(false);

  useEffect(() => { if (initialQ) search(); }, []);

  const search = async () => {
    if (!q.trim()) return;
    setLoading(true);
    const p = new URLSearchParams({ q, type });
    try { const r = await fetch(`${API_URL}/api/v1/search/?${p}`); if (r.ok) setResults(await r.json()); } catch {}
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 flex items-center gap-3"><Search className="w-8 h-8 text-blue-400" /> Qidiruv</h1>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6">
          <div className="flex gap-2">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input value={q} onChange={(e) => setQ(e.target.value)} onKeyDown={(e) => e.key === "Enter" && search()}
                placeholder="Startap, ish, xizmat, foydalanuvchi..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-blue-500 focus:outline-none" />
            </div>
            <button onClick={search} className="px-6 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl font-medium">Qidirish</button>
          </div>
          <div className="flex flex-wrap gap-2 mt-3">
            {["all", "users", "startups", "jobs", "services", "courses", "investors"].map(t => (
              <button key={t} onClick={() => { setType(t); search(); }} className={`px-3 py-1.5 rounded-lg text-sm capitalize ${type === t ? "bg-blue-500" : "bg-white/5"}`}>{t}</button>
            ))}
          </div>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div></div> :
        results.total === 0 && q ? <div className="text-center py-20 bg-white/5 rounded-2xl"><Search className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">"{q}" bo'yicha hech narsa topilmadi</p></div> :
        <div className="space-y-6">
          {results.users?.length > 0 && (
            <div>
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><Users className="w-5 h-5" /> Foydalanuvchilar ({results.users.length})</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {results.users.map((u: any) => (
                  <Link key={u.id} href={`/users/${u.id}`} className="flex items-center gap-3 p-3 bg-white/5 border border-white/10 rounded-xl hover:border-blue-500/50">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center font-bold">{u.full_name?.[0]}</div>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium truncate">{u.full_name}</div>
                      <div className="text-sm text-gray-400 truncate">@{u.username}</div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {results.startups?.length > 0 && (
            <div>
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><Rocket className="w-5 h-5" /> Startaplar ({results.startups.length})</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {results.startups.map((s: any) => (
                  <Link key={s.id} href={`/startups/${s.id}`} className="p-3 bg-white/5 border border-white/10 rounded-xl hover:border-blue-500/50">
                    <div className="font-medium">{s.name}</div>
                    <div className="text-sm text-gray-400 line-clamp-1">{s.tagline}</div>
                    <div className="flex gap-2 mt-1 text-xs text-gray-500"><span>{s.category}</span><span>•</span><span>{s.stage}</span></div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {results.jobs?.length > 0 && (
            <div>
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><Briefcase className="w-5 h-5" /> Ish o'rinlari ({results.jobs.length})</h2>
              <div className="space-y-2">
                {results.jobs.map((j: any) => (
                  <Link key={j.id} href={`/jobs?id=${j.id}`} className="block p-3 bg-white/5 border border-white/10 rounded-xl hover:border-blue-500/50">
                    <div className="font-medium">{j.title}</div>
                    <div className="text-sm text-gray-400">{j.location} • {j.job_type}</div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {results.services?.length > 0 && (
            <div>
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><Wrench className="w-5 h-5" /> Xizmatlar ({results.services.length})</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {results.services.map((s: any) => (
                  <Link key={s.id} href={`/services?id=${s.id}`} className="p-3 bg-white/5 border border-white/10 rounded-xl hover:border-blue-500/50">
                    <div className="font-medium">{s.title}</div>
                    <div className="text-sm text-yellow-400">{Math.round(s.price_basic).toLocaleString()} so'm dan</div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {results.courses?.length > 0 && (
            <div>
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><GraduationCap className="w-5 h-5" /> Kurslar ({results.courses.length})</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {results.courses.map((c: any) => (
                  <Link key={c.id} href={`/courses?id=${c.id}`} className="p-3 bg-white/5 border border-white/10 rounded-xl hover:border-blue-500/50">
                    <div className="font-medium">{c.title}</div>
                    <div className="text-sm text-gray-400">{c.level} • {c.price > 0 ? `${Math.round(c.price).toLocaleString()} so'm` : "Bepul"}</div>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {results.investors?.length > 0 && (
            <div>
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><TrendingUp className="w-5 h-5" /> Investorlar ({results.investors.length})</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {results.investors.map((i: any) => (
                  <Link key={i.id} href={`/investors?id=${i.id}`} className="p-3 bg-white/5 border border-white/10 rounded-xl hover:border-blue-500/50">
                    <div className="font-medium">{i.name}</div>
                    <div className="text-sm text-gray-400">{i.type} • ${i.min_investment.toLocaleString()}-${i.max_investment.toLocaleString()}</div>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>}
      </div>
    </div>
  );
}
