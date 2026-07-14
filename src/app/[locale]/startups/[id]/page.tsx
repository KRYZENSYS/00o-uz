"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { Rocket, MapPin, Globe, Heart, Eye, TrendingUp, Users, DollarSign, MessageSquare, Share2, ArrowLeft, Sparkles } from "lucide-react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function StartupDetailPage() {
  const params = useParams();
  const [s, setS] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [liked, setLiked] = useState(false);

  useEffect(() => { load(); }, [params.id]);

  const load = async () => {
    try {
      const r = await fetch(`${API_URL}/api/v1/startups/${params.id}`);
      if (r.ok) setS(await r.json());
    } catch {}
    setLoading(false);
  };

  const like = async () => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    const r = await fetch(`${API_URL}/api/v1/startups/${params.id}/like`, { method: "POST", headers: { Authorization: `Bearer ${t}` }});
    if (r.ok) { const d = await r.json(); setLiked(d.liked); load(); }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white"><div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div></div>;
  if (!s) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">Topilmadi</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-4xl mx-auto">
        <Link href="/startups" className="inline-flex items-center gap-2 text-gray-400 hover:text-white mb-4"><ArrowLeft className="w-4 h-4" /> Orqaga</Link>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl overflow-hidden">
          <div className="h-48 bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 relative">
            {s.is_featured && <div className="absolute top-4 right-4 px-3 py-1 bg-yellow-500 text-black rounded-full text-sm font-bold">⭐ Featured</div>}
          </div>
          <div className="px-6 pb-6 -mt-16">
            <div className="flex items-end gap-4 flex-wrap">
              <div className="w-28 h-28 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 border-4 border-slate-900 flex items-center justify-center text-4xl font-bold">
                {s.name[0]}
              </div>
              <div className="flex-1 pb-2">
                <h1 className="text-3xl font-bold flex items-center gap-2">
                  {s.name} {s.is_verified && <span className="text-blue-400">✓</span>}
                </h1>
                <p className="text-gray-300 mt-1">{s.tagline}</p>
                <div className="flex flex-wrap items-center gap-3 mt-2 text-sm text-gray-400">
                  {s.location && <span className="flex items-center gap-1"><MapPin className="w-4 h-4" />{s.location}</span>}
                  {s.website && <a href={s.website} target="_blank" className="flex items-center gap-1 text-purple-400"><Globe className="w-4 h-4" /> Website</a>}
                  <span className="px-2 py-0.5 bg-purple-500/20 text-purple-300 rounded">{s.category}</span>
                  <span className="px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded">{s.stage}</span>
                </div>
              </div>
              <div className="flex gap-2">
                <button onClick={like} className={`px-4 py-2 rounded-xl flex items-center gap-2 ${liked ? "bg-pink-500" : "bg-white/10"}`}>
                  <Heart className={`w-4 h-4 ${liked ? "fill-white" : ""}` /> {s.likes_count}
                </button>
                <button className="px-4 py-2 bg-white/10 rounded-xl flex items-center gap-2"><Share2 className="w-4 h-4" /> Ulashish</button>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3 mt-6">
              <div className="bg-white/5 border border-white/10 rounded-xl p-3 text-center">
                <Eye className="w-5 h-5 mx-auto mb-1 text-blue-400" />
                <div className="text-2xl font-bold">{s.views_count}</div>
                <div className="text-xs text-gray-400">Ko'rishlar</div>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-3 text-center">
                <Heart className="w-5 h-5 mx-auto mb-1 text-pink-400" />
                <div className="text-2xl font-bold">{s.likes_count}</div>
                <div className="text-xs text-gray-400">Yoqtirishlar</div>
              </div>
              <div className="bg-white/5 border border-white/10 rounded-xl p-3 text-center">
                <DollarSign className="w-5 h-5 mx-auto mb-1 text-green-400" />
                <div className="text-2xl font-bold">${(s.funding_raised / 1000).toFixed(0)}K</div>
                <div className="text-xs text-gray-400">Sarmoya</div>
              </div>
            </div>

            <div className="mt-6">
              <h2 className="text-xl font-bold mb-2">Batafsil</h2>
              <p className="text-gray-300 whitespace-pre-wrap">{s.description}</p>
            </div>

            <div className="mt-6 flex gap-3 flex-wrap">
              <button className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl font-bold flex items-center gap-2">
                <DollarSign className="w-5 h-5" /> Investitsiya qilish
              </button>
              <button className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl font-bold flex items-center gap-2">
                <MessageSquare className="w-5 h-5" /> Bog'lanish
              </button>
              <Link href={`/ai?tool=business-plan&input=${encodeURIComponent(s.name + " " + s.tagline)}`} className="px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl font-bold flex items-center gap-2">
                <Sparkles className="w-5 h-5" /> AI Tahlil
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
