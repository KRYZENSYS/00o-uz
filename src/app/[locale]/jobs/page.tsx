"use client";
import { useState, useEffect } from "react";
import { Briefcase, MapPin, Search, DollarSign, Clock, Building, Heart, Filter, X } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function JobsPage() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [jobType, setJobType] = useState("");
  const [isRemote, setIsRemote] = useState(false);
  const [selected, setSelected] = useState<any>(null);

  useEffect(() => { load(); }, [category, jobType, isRemote]);

  const load = async () => {
    setLoading(true);
    const p = new URLSearchParams();
    if (search) p.append("search", search);
    if (category) p.append("category", category);
    if (jobType) p.append("job_type", jobType);
    if (isRemote) p.append("is_remote", "true");
    try {
      const r = await fetch(`${API_URL}/api/v1/jobs?${p}`);
      setJobs(await r.json());
    } catch {}
    setLoading(false);
  };

  const apply = async (id: number) => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    const r = await fetch(`${API_URL}/api/v1/jobs/${id}/apply`, { method: "POST", headers: { Authorization: `Bearer ${t}` }});
    if (r.ok) alert("Arizangiz yuborildi!");
  };

  const formatSalary = (min: number, max: number, c: string) => {
    if (!min && !max) return "Kelishilgan holda";
    const f = (n: number) => n >= 1000000 ? `${(n/1000000).toFixed(1)}M` : `${(n/1000).toFixed(0)}K`;
    return `${f(min || 0)} - ${f(max || min || 0)} ${c}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold flex items-center gap-3"><Briefcase className="w-10 h-10 text-blue-400" /> Ish o'rinlari</h1>
          <p className="text-gray-400 mt-2">O'zbekistondagi eng yaxshi vakansiyalar</p>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6">
          <div className="flex flex-wrap gap-3">
            <div className="flex-1 min-w-[200px] relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && load()}
                placeholder="Lavozim, kompaniya..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-blue-500 focus:outline-none" />
            </div>
            <select value={category} onChange={(e) => setCategory(e.target.value)} className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
              <option value="">Barcha sohalar</option>
              <option value="it">IT</option>
              <option value="marketing">Marketing</option>
              <option value="sales">Sotuvlar</option>
              <option value="finance">Moliya</option>
              <option value="design">Dizayn</option>
              <option value="education">Ta'lim</option>
            </select>
            <select value={jobType} onChange={(e) => setJobType(e.target.value)} className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
              <option value="">Barcha turdagi</option>
              <option value="full_time">To'liq ish kuni</option>
              <option value="part_time">Yarim stavka</option>
              <option value="contract">Shartnoma</option>
              <option value="freelance">Masofaviy</option>
            </select>
            <label className="flex items-center gap-2 px-4 py-3 bg-white/5 border border-white/10 rounded-xl cursor-pointer">
              <input type="checkbox" checked={isRemote} onChange={(e) => setIsRemote(e.target.checked)} className="w-4 h-4" />
              <span>Faqat masofaviy</span>
            </label>
          </div>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div></div> :
        jobs.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><Briefcase className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">Ish o'rinlari topilmadi</p></div> :
        <div className="space-y-3">
          {jobs.map((j) => (
            <div key={j.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 hover:border-blue-500/50 transition">
              <div className="flex items-start justify-between flex-wrap gap-3">
                <div className="flex-1 min-w-[200px]">
                  <div className="flex items-center gap-2 mb-2 flex-wrap">
                    {j.is_featured && <span className="px-2 py-0.5 bg-yellow-500/20 text-yellow-400 text-xs rounded-full">⭐ Top</span>}
                    <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 text-xs rounded-full">{j.category}</span>
                    <span className="px-2 py-0.5 bg-purple-500/20 text-purple-300 text-xs rounded-full">{j.job_type === "full_time" ? "To'liq" : j.job_type}</span>
                    {j.is_remote && <span className="px-2 py-0.5 bg-green-500/20 text-green-300 text-xs rounded-full">🏠 Remote</span>}
                  </div>
                  <h3 className="text-xl font-bold mb-1 cursor-pointer hover:text-blue-400" onClick={() => setSelected(j)}>{j.title}</h3>
                  <div className="flex flex-wrap items-center gap-4 text-sm text-gray-400">
                    <span className="flex items-center gap-1"><Building className="w-4 h-4" />Kompaniya</span>
                    {j.location && <span className="flex items-center gap-1"><MapPin className="w-4 h-4" />{j.location}</span>}
                    <span className="flex items-center gap-1"><DollarSign className="w-4 h-4" />{formatSalary(j.salary_min, j.salary_max, j.currency)}</span>
                    <span className="flex items-center gap-1"><Clock className="w-4 h-4" />{new Date(j.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => setSelected(j)} className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-xl text-sm">Batafsil</button>
                  <button onClick={() => apply(j.id)} className="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl text-sm font-medium">Ariza</button>
                </div>
              </div>
            </div>
          ))}
        </div>}
      </div>

      {selected && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4" onClick={() => setSelected(null)}>
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-start justify-between mb-4">
              <h2 className="text-2xl font-bold">{selected.title}</h2>
              <button onClick={() => setSelected(null)}><X className="w-6 h-6" /></button>
            </div>
            <div className="space-y-3 text-sm">
              <p className="text-gray-300 whitespace-pre-wrap">{selected.description}</p>
              {selected.skills?.length > 0 && (
                <div>
                  <div className="text-gray-400 mb-1">Ko'nikmalar:</div>
                  <div className="flex flex-wrap gap-2">{selected.skills.map((s: string) => <span key={s} className="px-2 py-1 bg-white/10 rounded text-xs">{s}</span>)}</div>
                </div>
              )}
            </div>
            <button onClick={() => apply(selected.id)} className="w-full mt-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl font-bold">Arizani yuborish</button>
          </div>
        </div>
      )}
    </div>
  );
}
