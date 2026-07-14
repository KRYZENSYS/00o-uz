"use client";
import { useState, useEffect } from "react";
import { GraduationCap, Search, Users, Star, Clock, BookOpen, Play, Award } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function CoursesPage() {
  const [courses, setCourses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [level, setLevel] = useState("");

  useEffect(() => { load(); }, [category, level]);

  const load = async () => {
    setLoading(true);
    const p = new URLSearchParams();
    if (search) p.append("search", search);
    if (category) p.append("category", category);
    if (level) p.append("level", level);
    try { const r = await fetch(`${API_URL}/api/v1/courses/?${p}`); setCourses(await r.json()); } catch {}
    setLoading(false);
  };

  const enroll = async (id: number) => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    const r = await fetch(`${API_URL}/api/v1/courses/${id}/enroll`, { method: "POST", headers: { Authorization: `Bearer ${t}` }});
    if (r.ok) alert("Kursga yozildingiz!");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold flex items-center gap-3"><GraduationCap className="w-10 h-10 text-indigo-400" /> Kurslar</h1>
          <p className="text-gray-400 mt-2">Professional ko'nikmalarni o'rganing</p>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6 flex flex-wrap gap-3">
          <div className="flex-1 min-w-[200px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && load()}
              placeholder="Kurs qidirish..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-indigo-500 focus:outline-none" />
          </div>
          <select value={category} onChange={(e) => setCategory(e.target.value)} className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
            <option value="">Barcha kategoriyalar</option>
            <option value="programming">Dasturlash</option>
            <option value="design">Dizayn</option>
            <option value="marketing">Marketing</option>
            <option value="business">Biznes</option>
            <option value="ai">AI</option>
            <option value="language">Til</option>
          </select>
          <select value={level} onChange={(e) => setLevel(e.target.value)} className="px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
            <option value="">Barcha darajalar</option>
            <option value="beginner">Boshlang'ich</option>
            <option value="intermediate">O'rta</option>
            <option value="advanced">Yuqori</option>
          </select>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div></div> :
        courses.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><GraduationCap className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">Kurslar topilmadi</p></div> :
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {courses.map(c => (
            <div key={c.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden hover:border-indigo-500/50 transition group">
              <div className="h-40 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 relative overflow-hidden">
                {c.cover_image ? <img src={c.cover_image} alt={c.title} className="w-full h-full object-cover" /> : <div className="flex items-center justify-center h-full"><GraduationCap className="w-16 h-16 text-white/50" /></div>}
                {c.is_featured && <div className="absolute top-3 right-3 px-2 py-0.5 bg-yellow-500 text-black text-xs rounded-full font-bold">⭐ Top</div>}
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                <div className="absolute bottom-2 left-2 right-2 flex items-center gap-2 text-white text-xs">
                  <span className="px-2 py-0.5 bg-white/20 backdrop-blur rounded">{c.level}</span>
                  <span className="px-2 py-0.5 bg-white/20 backdrop-blur rounded">{c.category}</span>
                </div>
              </div>
              <div className="p-4">
                <h3 className="font-bold text-lg mb-1 line-clamp-2">{c.title}</h3>
                <p className="text-gray-400 text-sm mb-2 line-clamp-2">{c.description}</p>
                <div className="text-xs text-gray-500 mb-3">👨‍🏫 {c.instructor}</div>
                <div className="flex items-center gap-3 text-xs text-gray-400 mb-3">
                  <span className="flex items-center gap-1"><Users className="w-3 h-3" />{c.students_count}</span>
                  <span className="flex items-center gap-1"><Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />{c.rating || "5.0"}</span>
                  <span className="flex items-center gap-1"><BookOpen className="w-3 h-3" />{c.lessons_count} dars</span>
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{c.duration_hours?.toFixed(1)} soat</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="text-xl font-bold text-indigo-400">{c.price > 0 ? `${Math.round(c.price).toLocaleString()} so'm` : "Bepul"}</div>
                  <button onClick={() => enroll(c.id)} className="px-4 py-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg text-sm font-medium flex items-center gap-1">
                    <Play className="w-3 h-3" /> Boshlash
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>}
      </div>
    </div>
  );
}
