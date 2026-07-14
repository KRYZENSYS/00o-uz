"use client";
import { useState, useEffect } from "react";
import { Heart, MessageCircle, Share2, MoreHorizontal, Image as ImageIcon, Send, TrendingUp, X, Crown, BadgeCheck } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function FeedPage() {
  const [posts, setPosts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<"feed" | "trending">("feed");
  const [newPost, setNewPost] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [activeComments, setActiveComments] = useState<any>(null);
  const [comments, setComments] = useState<any[]>([]);
  const [newComment, setNewComment] = useState("");

  useEffect(() => { load(); }, [tab]);

  const load = async () => {
    setLoading(true);
    const t = localStorage.getItem("token");
    try {
      const r = await fetch(`${API_URL}/api/v1/posts/${tab}`, { headers: t ? { Authorization: `Bearer ${t}` } : {} });
      if (r.ok) setPosts(await r.json());
    } catch {}
    setLoading(false);
  };

  const like = async (id: number) => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    const r = await fetch(`${API_URL}/api/v1/posts/${id}/like`, { method: "POST", headers: { Authorization: `Bearer ${t}` }});
    if (r.ok) { const d = await r.json(); setPosts(p => p.map(x => x.id === id ? { ...x, is_liked: d.liked, likes_count: d.count } : x)); }
  };

  const create = async () => {
    if (!newPost.trim()) return;
    const t = localStorage.getItem("token");
    await fetch(`${API_URL}/api/v1/posts/`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ content: newPost, images: [], tags: [] }) });
    setNewPost(""); setShowCreate(false); load();
  };

  const openComments = async (post: any) => {
    setActiveComments(post);
    const t = localStorage.getItem("token");
    const r = await fetch(`${API_URL}/api/v1/posts/${post.id}`, { headers: t ? { Authorization: `Bearer ${t}` } : {} });
    if (r.ok) { const d = await r.json(); setComments(d.comments || []); }
  };

  const addComment = async () => {
    if (!newComment.trim() || !activeComments) return;
    const t = localStorage.getItem("token");
    const r = await fetch(`${API_URL}/api/v1/posts/${activeComments.id}/comments`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ content: newComment }) });
    if (r.ok) { setNewComment(""); openComments(activeComments); }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold">📱 Feed</h1>
          <button onClick={() => setShowCreate(true)} className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl font-medium">+ Post</button>
        </div>

        <div className="flex gap-2 mb-6 bg-white/5 p-1 rounded-xl">
          <button onClick={() => setTab("feed")} className={`flex-1 py-2 rounded-lg text-sm ${tab === "feed" ? "bg-purple-500" : "text-gray-400"}`}>Men uchun</button>
          <button onClick={() => setTab("trending")} className={`flex-1 py-2 rounded-lg text-sm flex items-center justify-center gap-1 ${tab === "trending" ? "bg-purple-500" : "text-gray-400"}`}><TrendingUp className="w-4 h-4" /> Trending</button>
        </div>

        {loading ? <div className="text-center py-20"><div className="inline-block w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div></div> :
        posts.length === 0 ? <div className="text-center py-20 bg-white/5 rounded-2xl"><p className="text-gray-400">Postlar yo'q</p></div> :
        <div className="space-y-4">
          {posts.map(p => (
            <div key={p.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center font-bold">{p.user.full_name?.[0]}</div>
                  <div>
                    <div className="font-semibold flex items-center gap-1">{p.user.full_name} {p.user.is_verified && <BadgeCheck className="w-4 h-4 text-blue-400" />} {p.user.is_premium && <Crown className="w-4 h-4 text-yellow-400" />}</div>
                    <div className="text-xs text-gray-400">@{p.user.username} • {new Date(p.created_at).toLocaleDateString()}</div>
                  </div>
                </div>
                <button className="p-1 hover:bg-white/10 rounded-lg"><MoreHorizontal className="w-5 h-5" /></button>
              </div>
              <p className="text-gray-200 mb-3 whitespace-pre-wrap">{p.content}</p>
              {p.images?.length > 0 && <div className="grid grid-cols-2 gap-2 mb-3">{p.images.map((img: string, i: number) => <img key={i} src={img} alt="" className="rounded-xl w-full" />)}</div>}
              {p.tags?.length > 0 && <div className="flex flex-wrap gap-1 mb-3">{p.tags.map((t: string) => <span key={t} className="text-purple-400 text-sm">#{t}</span>)}</div>}
              <div className="flex items-center gap-1 border-t border-white/10 pt-3">
                <button onClick={() => like(p.id)} className="flex-1 flex items-center justify-center gap-2 py-2 hover:bg-white/5 rounded-lg">
                  <Heart className={`w-5 h-5 ${p.is_liked ? "fill-pink-500 text-pink-500" : ""}`} /><span className="text-sm">{p.likes_count}</span>
                </button>
                <button onClick={() => openComments(p)} className="flex-1 flex items-center justify-center gap-2 py-2 hover:bg-white/5 rounded-lg">
                  <MessageCircle className="w-5 h-5" /><span className="text-sm">{p.comments_count}</span>
                </button>
                <button className="flex-1 flex items-center justify-center gap-2 py-2 hover:bg-white/5 rounded-lg">
                  <Share2 className="w-5 h-5" /><span className="text-sm">{p.shares_count}</span>
                </button>
              </div>
            </div>
          ))}
        </div>}
      </div>

      {showCreate && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur flex items-center justify-center p-4" onClick={() => setShowCreate(false)}>
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-lg w-full" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold">Yangi post</h2>
              <button onClick={() => setShowCreate(false)}><X className="w-5 h-5" /></button>
            </div>
            <textarea value={newPost} onChange={(e) => setNewPost(e.target.value)} rows={5} placeholder="Nima haqida o'ylayapsiz?" className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl mb-3 focus:outline-none focus:border-purple-500" />
            <div className="flex justify-between items-center">
              <button className="p-2 hover:bg-white/10 rounded-lg"><ImageIcon className="w-5 h-5" /></button>
              <button onClick={create} className="px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl font-medium">Joylash</button>
            </div>
          </div>
        </div>
      )}

      {activeComments && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur flex items-end md:items-center justify-center" onClick={() => setActiveComments(null)}>
          <div className="bg-slate-900 border-t md:border border-white/10 rounded-t-2xl md:rounded-2xl p-4 max-w-lg w-full max-h-[80vh] flex flex-col" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-3 pb-3 border-b border-white/10">
              <h3 className="font-bold">Izohlar</h3>
              <button onClick={() => setActiveComments(null)}><X className="w-5 h-5" /></button>
            </div>
            <div className="flex-1 overflow-y-auto space-y-3 mb-3">
              {comments.map((c: any) => (
                <div key={c.id} className="flex gap-2">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-sm font-bold flex-shrink-0">{c.user.full_name?.[0]}</div>
                  <div className="flex-1 bg-white/5 rounded-2xl p-3">
                    <div className="text-sm font-semibold">{c.user.full_name}</div>
                    <p className="text-sm text-gray-200">{c.content}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="flex gap-2 pt-2 border-t border-white/10">
              <input value={newComment} onChange={(e) => setNewComment(e.target.value)} onKeyDown={(e) => e.key === "Enter" && addComment()} placeholder="Izoh yozing..." className="flex-1 px-4 py-2 bg-white/5 border border-white/10 rounded-full text-sm" />
              <button onClick={addComment} className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"><Send className="w-4 h-4" /></button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
