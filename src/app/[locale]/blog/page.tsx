"use client";
import { useState, useEffect } from "react";
import { BookOpen, Search, Eye, Heart, Calendar, User as UserIcon, Plus, TrendingUp, Filter, X, Send, MessageCircle } from "lucide-react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function BlogPage() {
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [activePost, setActivePost] = useState<any>(null);
  const [comment, setComment] = useState("");

  useEffect(() => { load(); }, [category]);

  const load = async () => {
    setLoading(true);
    const p = new URLSearchParams();
    if (search) p.append("search", search);
    if (category) p.append("category", category);
    try { const r = await fetch(`${API_URL}/api/v1/marketing/blog/posts?${p}`); if (r.ok) setPosts(await r.json()); } catch {}
    setLoading(false);
  };

  const openPost = async (slug: string) => {
    const r = await fetch(`${API_URL}/api/v1/marketing/blog/posts/${slug}`);
    if (r.ok) setActivePost(await r.json());
  };

  const like = async (id: number) => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    await fetch(`${API_URL}/api/v1/marketing/blog/posts/${id}/like`, { method: "POST", headers: { Authorization: `Bearer ${t}` } });
  };

  const categories = [
    { id: "", name: "Hammasi", icon: "📚" },
    { id: "startup", name: "Startaplar", icon: "🚀" },
    { id: "tech", name: "Texnologiya", icon: "💻" },
    { id: "ai", name: "AI", icon: "🤖" },
    { id: "marketing", name: "Marketing", icon: "📈" },
    { id: "career", name: "Karyera", icon: "💼" },
    { id: "design", name: "Dizayn", icon: "🎨" },
    { id: "finance", name: "Moliya", icon: "💰" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 text-white p-4 md:p-6">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
          <div>
            <h1 className="text-4xl font-bold flex items-center gap-3"><BookOpen className="w-10 h-10 text-indigo-400" /> Blog</h1>
            <p className="text-gray-400 mt-1">Foydali maqolalar, yangiliklar, tajribalar</p>
          </div>
          <Link href="/blog/new" className="px-5 py-2.5 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl font-medium flex items-center gap-2"><Plus className="w-4 h-4" /> Maqola yozish</Link>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6">
          <div className="relative mb-3">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && load()} placeholder="Maqola qidirish..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="flex gap-2 overflow-x-auto pb-2">
            {categories.map(c => (
              <button key={c.id} onClick={() => setCategory(c.id)} className={`px-3 py-2 rounded-lg text-sm whitespace-nowrap flex items-center gap-1 ${category === c.id ? "bg-indigo-500" : "bg-white/5"}`}>
                <span>{c.icon}</span> {c.name}
              </button>
            ))}
          </div>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div></div> :
        posts.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><BookOpen className="w-16 h-16 mx-auto text-gray-600 mb-4" /><p className="text-gray-400">Maqolalar topilmadi</p></div> :
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {posts.map(p => (
            <div key={p.id} onClick={() => openPost(p.slug)} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden hover:border-indigo-500/50 transition cursor-pointer group">
              <div className="h-44 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 relative">
                {p.cover_image ? <img src={p.cover_image} alt={p.title} className="w-full h-full object-cover" /> : <div className="flex items-center justify-center h-full text-6xl">📝</div>}
                <div className="absolute top-3 left-3 px-2 py-0.5 bg-black/40 backdrop-blur text-xs rounded-full">{p.category}</div>
              </div>
              <div className="p-4">
                <h2 className="font-bold text-lg mb-2 line-clamp-2 group-hover:text-indigo-400 transition">{p.title}</h2>
                <p className="text-sm text-gray-400 line-clamp-2 mb-3">{p.excerpt}</p>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-xs font-bold">{p.author?.[0]}</div>
                    <span>{p.author}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="flex items-center gap-1"><Eye className="w-3 h-3" />{p.views_count}</span>
                    <span className="flex items-center gap-1"><Heart className="w-3 h-3" />{p.likes_count}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>}
      </div>

      {activePost && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur flex items-center justify-center p-4" onClick={() => setActivePost(null)}>
          <div className="bg-slate-900 border border-white/10 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="sticky top-0 bg-slate-900 border-b border-white/10 p-4 flex items-center justify-between">
              <h2 className="font-bold">{activePost.title}</h2>
              <button onClick={() => setActivePost(null)}><X className="w-5 h-5" /></button>
            </div>
            <div className="p-6">
              {activePost.cover_image && <img src={activePost.cover_image} alt="" className="w-full h-64 object-cover rounded-xl mb-4" />}
              <div className="flex items-center gap-3 mb-4 text-sm text-gray-400">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center">{activePost.author.full_name?.[0]}</div>
                <div>
                  <div className="font-medium text-white">{activePost.author.full_name}</div>
                  <div className="text-xs">{activePost.published_at?.split('T')[0]}</div>
                </div>
                <div className="ml-auto flex items-center gap-3">
                  <button onClick={() => like(activePost.id)} className="flex items-center gap-1 hover:text-pink-400"><Heart className="w-4 h-4" /> {activePost.likes_count}</button>
                  <span className="flex items-center gap-1"><Eye className="w-4 h-4" /> {activePost.views_count}</span>
                </div>
              </div>
              <div className="prose prose-invert max-w-none text-gray-200 whitespace-pre-wrap">{activePost.content}</div>
              <div className="mt-6 pt-6 border-t border-white/10">
                <h3 className="font-bold mb-3 flex items-center gap-2"><MessageCircle className="w-4 h-4" /> Izohlar</h3>
                <div className="flex gap-2">
                  <input value={comment} onChange={(e) => setComment(e.target.value)} placeholder="Izoh yozing..." className="flex-1 px-4 py-2 bg-white/5 border border-white/10 rounded-full text-sm" />
                  <button className="p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"><Send className="w-4 h-4" /></button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
