"use client";
import { useState, useEffect } from "react";
import { Sparkles, Send, History, Crown, Wand2, Languages, Briefcase, Code2, FileText, Megaphone, Wrench, BarChart3, Mic } from "lucide-react";
import { useSearchParams } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const TOOLS = [
  { id: "chat", name: "AI Chat", icon: Wand2, color: "from-purple-500 to-pink-500", desc: "Umumiy suhbat" },
  { id: "business-plan", name: "Biznes reja", icon: Briefcase, color: "from-blue-500 to-cyan-500", desc: "Professional reja" },
  { id: "pitch-deck", name: "Pitch deck", icon: FileText, color: "from-green-500 to-emerald-500", desc: "Investorlar uchun" },
  { id: "startup-ideas", name: "Startap g'oyalar", icon: Sparkles, color: "from-yellow-500 to-orange-500", desc: "Kreativ g'oyalar" },
  { id: "resume", name: "Resume", icon: FileText, color: "from-indigo-500 to-purple-500", desc: "Professional CV" },
  { id: "cover-letter", name: "Cover Letter", icon: FileText, color: "from-pink-500 to-rose-500", desc: "Ish uchun" },
  { id: "marketing", name: "Marketing", icon: Megaphone, color: "from-red-500 to-pink-500", desc: "Strategiya" },
  { id: "seo", name: "SEO", icon: BarChart3, color: "from-cyan-500 to-blue-500", desc: "Qidiruv optimallashtirish" },
  { id: "blog", name: "Blog post", icon: FileText, color: "from-emerald-500 to-green-500", desc: "Maqola yozish" },
  { id: "code", name: "Kod", icon: Code2, color: "from-slate-500 to-slate-700", desc: "Dasturlash" },
  { id: "fix-bug", name: "Bug fix", icon: Wrench, color: "from-red-500 to-orange-500", desc: "Xatolarni tuzatish" },
  { id: "sql", name: "SQL", icon: Code2, color: "from-blue-600 to-indigo-600", desc: "Database so'rovlar" },
  { id: "translate", name: "Tarjimon", icon: Languages, color: "from-violet-500 to-purple-500", desc: "100+ til" },
  { id: "summarize", name: "Xulosa", icon: FileText, color: "from-teal-500 to-cyan-500", desc: "Matn qisqartirish" },
  { id: "brainstorm", name: "Brainstorm", icon: Sparkles, color: "from-amber-500 to-yellow-500", desc: "G'oyalar generatsiyasi" },
  { id: "planner", name: "Planner", icon: FileText, color: "from-rose-500 to-pink-500", desc: "Loyiha rejasi" },
  { id: "financial", name: "Moliyaviy", icon: BarChart3, color: "from-green-600 to-emerald-600", desc: "Tahlil" },
  { id: "competitor", name: "Raqobatchi", icon: BarChart3, color: "from-orange-500 to-red-500", desc: "Tahlil" },
  { id: "swot", name: "SWOT", icon: BarChart3, color: "from-fuchsia-500 to-pink-500", desc: "Tahlil" },
  { id: "legal", name: "Yuridik", icon: FileText, color: "from-gray-500 to-slate-600", desc: "Maslahat" }
];

export default function AIPage() {
  const params = useSearchParams();
  const initialTool = params.get("tool") || "chat";
  const initialInput = params.get("input") || "";
  
  const [tool, setTool] = useState(initialTool);
  const [input, setInput] = useState(initialInput);
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<any[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => { loadHistory(); }, []);

  const loadHistory = async () => {
    const t = localStorage.getItem("token");
    if (!t) return;
    try { const r = await fetch(`${API_URL}/api/v1/ai/history?limit=20`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setHistory(await r.json()); } catch {}
  };

  const run = async () => {
    if (!input.trim() || loading) return;
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    setLoading(true); setOutput("");
    try {
      const r = await fetch(`${API_URL}/api/v1/ai/execute`, {
        method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" },
        body: JSON.stringify({ tool, input, language: "uz" })
      });
      const d = await r.json();
      setOutput(d.output || d.error || "Xatolik");
      loadHistory();
    } catch { setOutput("Ulanish xatoligi"); }
    setLoading(false);
  };

  const activeTool = TOOLS.find(t => t.id === tool) || TOOLS[0];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-4 md:p-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3"><Sparkles className="w-8 h-8 text-purple-400" /> AI Yordamchi</h1>
            <p className="text-gray-400 mt-1">30+ AI vosita — tez, kuchli, professional</p>
          </div>
          <button onClick={() => setShowHistory(!showHistory)} className="px-4 py-2 bg-white/10 rounded-xl flex items-center gap-2"><History className="w-4 h-4" /> Tarix</button>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-2 mb-6">
          {TOOLS.map(t => { const Icon = t.icon; return (
            <button key={t.id} onClick={() => setTool(t.id)} className={`p-3 rounded-xl text-left transition ${tool === t.id ? `bg-gradient-to-br ${t.color}` : "bg-white/5 hover:bg-white/10"}`}>
              <Icon className="w-5 h-5 mb-1" />
              <div className="text-sm font-medium">{t.name}</div>
            </button>
          );})}
        </div>

        <div className="grid lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2 bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5">
            <div className="flex items-center gap-3 mb-3 pb-3 border-b border-white/10">
              <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${activeTool.color} flex items-center justify-center`}><activeTool.icon className="w-5 h-5" /></div>
              <div>
                <div className="font-bold">{activeTool.name}</div>
                <div className="text-xs text-gray-400">{activeTool.desc}</div>
              </div>
            </div>
            <textarea value={input} onChange={(e) => setInput(e.target.value)} rows={6} placeholder="Savolingizni yozing..." className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:outline-none focus:border-purple-500 resize-none" />
            <button onClick={run} disabled={loading} className="w-full mt-3 py-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl font-bold disabled:opacity-50 flex items-center justify-center gap-2">
              {loading ? <><div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" /> AI ishlayapti...</> : <><Send className="w-5 h-5" /> Yuborish</>}
            </button>
            {output && (
              <div className="mt-5 pt-5 border-t border-white/10">
                <div className="text-sm text-gray-400 mb-2 flex items-center gap-2"><Sparkles className="w-4 h-4" /> Natija:</div>
                <div className="bg-black/30 rounded-xl p-4 text-sm whitespace-pre-wrap max-h-[500px] overflow-y-auto">{output}</div>
              </div>
            )}
          </div>

          {showHistory && (
            <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-5 max-h-[700px] overflow-y-auto">
              <h3 className="font-bold mb-3 flex items-center gap-2"><History className="w-4 h-4" /> Tarix</h3>
              {history.length === 0 ? <p className="text-sm text-gray-400">Tarix bo'sh</p> :
                <div className="space-y-2">
                  {history.map((h: any) => (
                    <div key={h.id} onClick={() => { setTool(h.tool); setInput(h.input); setOutput(h.output); }} className="p-3 bg-white/5 rounded-lg cursor-pointer hover:bg-white/10 text-sm">
                      <div className="font-medium text-purple-300">{h.tool}</div>
                      <div className="text-gray-400 line-clamp-2 text-xs mt-1">{h.input}</div>
                    </div>
                  ))}
                </div>}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
