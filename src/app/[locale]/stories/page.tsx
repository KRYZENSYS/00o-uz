"use client";
import { useState, useEffect } from "react";
import { Plus, X, ChevronLeft, ChevronRight, Eye, Heart, MoreHorizontal, Send } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function StoriesPage() {
  const [stories, setStories] = useState<any[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [currentStoryIndex, setCurrentStoryIndex] = useState(0);
  const [viewing, setViewing] = useState<any>(null);
  const [creating, setCreating] = useState(false);
  const [text, setText] = useState("");

  useEffect(() => { load(); }, []);

  const load = async () => {
    const t = localStorage.getItem("token");
    try { const r = await fetch(`${API_URL}/api/v1/stories/`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setStories(await r.json()); } catch {}
  };

  const view = (group: any) => setViewing(group);

  useEffect(() => {
    if (!viewing) return;
    const timer = setTimeout(() => {
      if (currentStoryIndex < viewing.stories.length - 1) setCurrentStoryIndex(i => i + 1);
      else {
        if (currentIndex < stories.length - 1) { setCurrentIndex(i => i + 1); setCurrentStoryIndex(0); setViewing(stories[currentIndex + 1]); }
        else { setViewing(null); setCurrentIndex(0); setCurrentStoryIndex(0); }
      }
    }, 5000);
    return () => clearTimeout(timer);
  }, [viewing, currentStoryIndex]);

  useEffect(() => {
    if (viewing && viewing.stories[currentStoryIndex]) {
      const t = localStorage.getItem("token");
      fetch(`${API_URL}/api/v1/stories/${viewing.stories[currentStoryIndex].id}/view`, { method: "POST", headers: { Authorization: `Bearer ${t}` } });
    }
  }, [viewing, currentStoryIndex]);

  const createTextStory = async () => {
    const t = localStorage.getItem("token");
    await fetch(`${API_URL}/api/v1/stories/`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ media_type: "text", text, background_color: "#7c3aed" }) });
    setText(""); setCreating(false); load();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-pink-900 to-slate-900 text-white p-4 md:p-6">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-6 flex items-center justify-between">
          Stories
          <button onClick={() => setCreating(true)} className="px-4 py-2 bg-gradient-to-r from-pink-500 to-purple-500 rounded-xl text-sm flex items-center gap-1"><Plus className="w-4 h-4" /> Yaratish</button>
        </h1>

        <div className="flex gap-3 overflow-x-auto pb-4 mb-4 scrollbar-hide">
          <div onClick={() => setCreating(true)} className="flex-shrink-0 w-16 h-16 rounded-full bg-gradient-to-br from-gray-700 to-gray-900 border-2 border-dashed border-white/30 flex items-center justify-center cursor-pointer">
            <Plus className="w-6 h-6" />
          </div>
          {stories.map((g, i) => (
            <div key={i} onClick={() => { setCurrentIndex(i); setCurrentStoryIndex(0); view(g); }} className="flex-shrink-0 cursor-pointer">
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-pink-500 via-purple-500 to-blue-500 p-0.5">
                <div className="w-full h-full rounded-full bg-slate-900 p-0.5">
                  <div className="w-full h-full rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-xl font-bold">{g.user.full_name?.[0]}</div>
                </div>
              </div>
              <div className="text-xs text-center mt-1 truncate w-16">{g.user.username}</div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {stories.flatMap(g => g.stories).map((s: any) => (
            <div key={s.id} className="aspect-[9/16] rounded-2xl overflow-hidden relative bg-gradient-to-br from-pink-500 to-purple-500">
              {s.media_type === "text" ? <div className="flex items-center justify-center h-full p-4 text-center font-bold text-2xl">{s.text}</div> : s.media_url ? <img src={s.media_url} alt="" className="w-full h-full object-cover" /> : <div className="flex items-center justify-center h-full">📷</div>}
              <div className="absolute bottom-2 left-2 right-2 text-xs flex items-center justify-between">
                <span className="flex items-center gap-1"><Eye className="w-3 h-3" />{s.views_count}</span>
                <span>{new Date(s.created_at).toLocaleTimeString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {viewing && (
        <div className="fixed inset-0 z-50 bg-black flex items-center justify-center" onClick={() => setViewing(null)}>
          <div className="relative w-full max-w-md h-full md:h-[90vh] md:rounded-2xl overflow-hidden" onClick={(e) => e.stopPropagation()}>
            <div className="absolute top-0 left-0 right-0 z-10 flex gap-1 p-2">
              {viewing.stories.map((_: any, i: number) => (
                <div key={i} className="flex-1 h-0.5 bg-white/30 rounded">
                  <div className="h-full bg-white rounded transition-all" style={{ width: i < currentStoryIndex ? "100%" : i === currentStoryIndex ? "50%" : "0%" }}></div>
                </div>
              ))}
            </div>
            <div className="absolute top-4 left-4 right-4 z-10 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-sm font-bold">{viewing.user.full_name?.[0]}</div>
                <div className="text-sm font-medium">{viewing.user.username}</div>
              </div>
              <button onClick={() => setViewing(null)} className="p-1"><X className="w-6 h-6" /></button>
            </div>
            <div className="h-full flex items-center justify-center text-center p-8" style={{ background: viewing.stories[currentStoryIndex]?.background_color || "#000" }}>
              <div className="text-3xl font-bold whitespace-pre-wrap">{viewing.stories[currentStoryIndex]?.text}</div>
            </div>
            <button onClick={() => currentStoryIndex > 0 && setCurrentStoryIndex(i => i - 1)} className="absolute left-2 top-1/2 -translate-y-1/2 p-2"><ChevronLeft className="w-8 h-8" /></button>
            <button onClick={() => currentStoryIndex < viewing.stories.length - 1 && setCurrentStoryIndex(i => i + 1)} className="absolute right-2 top-1/2 -translate-y-1/2 p-2"><ChevronRight className="w-8 h-8" /></button>
            <div className="absolute bottom-4 left-4 right-4 flex items-center gap-2">
              <input placeholder="Javob yozing..." className="flex-1 px-4 py-2 bg-white/20 backdrop-blur rounded-full text-sm" />
              <button className="p-2"><Heart className="w-6 h-6" /></button>
              <button className="p-2"><Send className="w-5 h-5" /></button>
            </div>
          </div>
        </div>
      )}

      {creating && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur flex items-center justify-center p-4" onClick={() => setCreating(false)}>
          <div className="bg-slate-900 border border-white/10 rounded-2xl p-6 max-w-md w-full" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-xl font-bold mb-4">Yangi story</h2>
            <textarea value={text} onChange={(e) => setText(e.target.value)} rows={4} placeholder="Nima yangilik?" className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-pink-500" />
            <div className="flex gap-2 mt-3">
              <button onClick={createTextStory} className="flex-1 py-2 bg-gradient-to-r from-pink-500 to-purple-500 rounded-xl font-medium">Joylash</button>
              <button onClick={() => setCreating(false)} className="px-4 py-2 bg-white/10 rounded-xl">Bekor</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
