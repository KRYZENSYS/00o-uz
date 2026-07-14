"use client";
import { useState, useEffect } from "react";
import { Sparkles, Wand2, Image as ImageIcon, Mic, Video, Palette, Download, Loader2 } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const TOOLS = [
  { id: "image", name: "Rasm yaratish", icon: ImageIcon, cost: 30, model: "DALL-E 3", color: "from-purple-500 to-pink-500", desc: "Matndan rasm" },
  { id: "logo", name: "Logo yaratish", icon: Palette, cost: 50, model: "DALL-E 3", color: "from-blue-500 to-cyan-500", desc: "Brend logotipi" },
  { id: "avatar", name: "Avatar yaratish", icon: Wand2, cost: 30, model: "DALL-E 3", color: "from-pink-500 to-rose-500", desc: "Profil rasmi" },
  { id: "thumbnail", name: "YouTube Thumbnail", icon: ImageIcon, cost: 40, model: "DALL-E 3", color: "from-red-500 to-orange-500", desc: "Video muqova" },
  { id: "video", name: "Video yaratish", icon: Video, cost: 100, model: "Sora", color: "from-violet-500 to-purple-500", desc: "AI video 5s" },
  { id: "tts", name: "Ovoz yaratish", icon: Mic, cost: 10, model: "ElevenLabs", color: "from-green-500 to-emerald-500", desc: "Matndan nutq" },
];

export default function AIMediaPage() {
  const [tool, setTool] = useState("image");
  const [prompt, setPrompt] = useState("");
  const [voice, setVoice] = useState("alloy");
  const [text, setText] = useState("");
  const [brandName, setBrandName] = useState("");
  const [industry, setIndustry] = useState("");
  const [loading, setLoading] = useState(false);
  const [gallery, setGallery] = useState<any[]>([]);
  const [result, setResult] = useState<any>(null);

  useEffect(() => { loadGallery(); }, []);

  const loadGallery = async () => {
    const t = localStorage.getItem("token");
    try { const r = await fetch(`${API_URL}/api/v1/ai-media/gallery`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setGallery(await r.json()); } catch {}
  };

  const generate = async () => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    setLoading(true); setResult(null);
    try {
      let r;
      if (tool === "image") r = await fetch(`${API_URL}/api/v1/ai-media/image`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ prompt, model: "dall-e-3", size: "1024x1024" }) });
      else if (tool === "logo") r = await fetch(`${API_URL}/api/v1/ai-media/logo`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ brand_name: brandName, industry }) });
      else if (tool === "avatar") r = await fetch(`${API_URL}/api/v1/ai-media/avatar`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ style: "professional" }) });
      else if (tool === "thumbnail") r = await fetch(`${API_URL}/api/v1/ai-media/thumbnail`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ title: prompt, style: "youtube" }) });
      else if (tool === "video") r = await fetch(`${API_URL}/api/v1/ai-media/video`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ prompt, duration: 5 }) });
      else if (tool === "tts") r = await fetch(`${API_URL}/api/v1/ai-media/audio/tts`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ text, voice }) });
      if (r?.ok) { setResult(await r.json()); loadGallery(); }
    } catch (e) { alert("Xatolik: " + e); }
    setLoading(false);
  };

  const activeTool = TOOLS.find(t => t.id === tool)!;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-fuchsia-900 to-slate-900 text-white p-4 md:p-6">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold flex items-center justify-center gap-3 mb-2"><Sparkles className="w-10 h-10 text-fuchsia-400" /> AI Media Studio</h1>
          <p className="text-gray-400">Rasmlar, logotiplar, videolar, ovozlar — hammasi AI bilan</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-6 gap-3 mb-6">
          {TOOLS.map(t => { const Icon = t.icon; return (
            <button key={t.id} onClick={() => setTool(t.id)} className={`p-4 rounded-2xl text-left transition ${tool === t.id ? `bg-gradient-to-br ${t.color} scale-105` : "bg-white/5 hover:bg-white/10"}`}>
              <Icon className="w-6 h-6 mb-2" />
              <div className="font-bold text-sm">{t.name}</div>
              <div className="text-xs opacity-80">{t.cost} 🪙</div>
            </button>
          );})}
        </div>

        <div className="grid lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-4 pb-3 border-b border-white/10">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${activeTool.color} flex items-center justify-center`}><activeTool.icon className="w-6 h-6" /></div>
              <div>
                <div className="font-bold text-lg">{activeTool.name}</div>
                <div className="text-xs text-gray-400">{activeTool.model} • {activeTool.cost} token</div>
              </div>
            </div>

            {tool === "image" || tool === "thumbnail" || tool === "video" ? (
              <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={5} placeholder={tool === "image" ? "Yaratmoqchi bo'lgan rasmni tavsiflang..." : tool === "thumbnail" ? "Video sarlavhasi..." : "Video uchun tavsif..."} className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-fuchsia-500 resize-none mb-3" />
            ) : tool === "logo" ? (
              <div className="space-y-3">
                <input value={brandName} onChange={(e) => setBrandName(e.target.value)} placeholder="Brend nomi" className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-fuchsia-500" />
                <input value={industry} onChange={(e) => setIndustry(e.target.value)} placeholder="Soha (masalan: texnologiya)" className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-fuchsia-500" />
              </div>
            ) : tool === "avatar" ? null : tool === "tts" ? (
              <div className="space-y-3">
                <textarea value={text} onChange={(e) => setText(e.target.value)} rows={5} placeholder="Matnni kiriting..." className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-fuchsia-500 resize-none" />
                <select value={voice} onChange={(e) => setVoice(e.target.value)} className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl">
                  <option value="alloy">Alloy (Universal)</option>
                  <option value="echo">Echo (Erkak)</option>
                  <option value="fable">Fable (Erkak, Britan)</option>
                  <option value="onyx">Onyx (Erkak, Chuqur)</option>
                  <option value="nova">Nova (Ayol)</option>
                  <option value="shimmer">Shimmer (Ayol)</option>
                </select>
              </div>
            ) : null}

            <button onClick={generate} disabled={loading} className={`w-full mt-4 py-4 bg-gradient-to-r ${activeTool.color} rounded-xl font-bold text-lg disabled:opacity-50 flex items-center justify-center gap-2`}>
              {loading ? <><Loader2 className="w-5 h-5 animate-spin" /> Yaratilmoqda...</> : <><Sparkles className="w-5 h-5" /> Yaratish</>}
            </button>

            {result && (
              <div className="mt-5 pt-5 border-t border-white/10">
                <div className="bg-green-500/20 border border-green-500/30 rounded-xl p-4 text-center">
                  <div className="text-green-400 font-bold mb-1">✅ Muvaffaqiyat!</div>
                  <div className="text-sm text-gray-300">ID: {result.id}</div>
                  {result.prompt && <div className="text-xs text-gray-400 mt-1">{result.prompt}</div>}
                </div>
              </div>
            )}
          </div>

          <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 max-h-[700px] overflow-y-auto">
            <h3 className="font-bold mb-3 flex items-center gap-2"><ImageIcon className="w-4 h-4" /> Galereya</h3>
            {gallery.length === 0 ? <p className="text-sm text-gray-400">Hozircha bo'sh</p> :
              <div className="space-y-3">
                {gallery.map((g: any) => (
                  <div key={g.id} className="bg-white/5 rounded-xl p-2">
                    <div className="aspect-square rounded-lg bg-gradient-to-br from-fuchsia-500/20 to-pink-500/20 flex items-center justify-center text-3xl">
                      {g.type === "image" ? "🖼" : g.type === "video" ? "🎬" : g.type === "audio" ? "🎵" : "📁"}
                    </div>
                    <div className="text-xs text-gray-400 mt-2 line-clamp-2">{g.prompt}</div>
                    <div className="text-xs text-gray-500 mt-1">{g.model} • {g.status}</div>
                  </div>
                ))}
              </div>}
          </div>
        </div>
      </div>
    </div>
  );
}
