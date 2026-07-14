"use client";
import { useState, useRef, useEffect } from "react";
import { Send, Sparkles, Loader2, Wand2, Code, Languages, FileText, BarChart3, Lightbulb, Briefcase, Image as ImageIcon, Music, Mic, Paperclip, Copy, Check, Trash2 } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const TOOLS = [
  { id: "chat", name: "AI Chat", icon: Sparkles, color: "from-blue-500 to-cyan-500", desc: "Erkin suhbat" },
  { id: "business-plan", name: "Biznes reja", icon: FileText, color: "from-purple-500 to-pink-500", desc: "To'liq reja" },
  { id: "pitch-deck", name: "Pitch deck", icon: BarChart3, color: "from-orange-500 to-red-500", desc: "Investorlar uchun" },
  { id: "startup-ideas", name: "G'oyalar", icon: Lightbulb, color: "from-yellow-500 to-orange-500", desc: "10 ta g'oya" },
  { id: "code", name: "Kod", icon: Code, color: "from-green-500 to-emerald-500", desc: "Kod generatori" },
  { id: "translate", name: "Tarjimon", icon: Languages, color: "from-pink-500 to-rose-500", desc: "100+ til" },
  { id: "resume", name: "Resume", icon: Briefcase, color: "from-indigo-500 to-purple-500", desc: "CV builder" },
  { id: "marketing", name: "Marketing", icon: Wand2, color: "from-teal-500 to-cyan-500", desc: "Strategiya" },
  { id: "image", name: "Rasm", icon: ImageIcon, color: "from-fuchsia-500 to-pink-500", desc: "AI image" },
  { id: "music", name: "Musiqa", icon: Music, color: "from-amber-500 to-yellow-500", desc: "AI music" },
  { id: "voice", name: "Ovoz", icon: Mic, color: "from-violet-500 to-purple-500", desc: "Voice AI" },
  { id: "summarize", name: "Xulosa", icon: FileText, color: "from-sky-500 to-blue-500", desc: "Qisqartirish" },
];

export default function AIPage() {
  const [messages, setMessages] = useState([{ role: "assistant", content: "👋 Salom! Men 00o.uz AI yordamchiman. 30+ vosita orqali yordam bera olaman. Qaysi birini sinab ko'ramiz?", tool: "chat" }]);
  const [input, setInput] = useState("");
  const [selectedTool, setSelectedTool] = useState("chat");
  const [loading, setLoading] = useState(false);
  const [copiedIdx, setCopiedIdx] = useState<number | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => { scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" }); }, [messages]);

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg = { role: "user", content: input, tool: selectedTool };
    setMessages(m => [...m, userMsg]);
    const cur = input; setInput(""); setLoading(true);
    try {
      const r = await fetch(`${API_URL}/api/v1/ai/execute`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tool: selectedTool, input: cur, language: "uz" })
      });
      const d = await r.json();
      setMessages(m => [...m, { role: "assistant", content: d.content || "Xatolik", tool: selectedTool }]);
    } catch {
      setMessages(m => [...m, { role: "assistant", content: "❌ Xatolik yuz berdi.", tool: selectedTool }]);
    }
    setLoading(false);
  };

  const copy = (t: string, i: number) => { navigator.clipboard.writeText(t); setCopiedIdx(i); setTimeout(() => setCopiedIdx(null), 2000); };
  const clear = () => setMessages([{ role: "assistant", content: "Chat tozalandi!", tool: "chat" }]);
  const currentTool = TOOLS.find(t => t.id === selectedTool)!;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 text-white">
      <div className="max-w-7xl mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-4 h-screen">
        <aside className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 overflow-y-auto">
          <h2 className="font-bold text-lg mb-3 flex items-center gap-2"><Sparkles className="w-5 h-5 text-purple-400" /> AI Vositalar</h2>
          <div className="space-y-2">
            {TOOLS.map(t => {
              const Icon = t.icon;
              return (
                <button key={t.id} onClick={() => setSelectedTool(t.id)}
                  className={`w-full text-left p-3 rounded-xl transition flex items-center gap-3 ${selectedTool === t.id ? `bg-gradient-to-r ${t.color}` : "bg-white/5 hover:bg-white/10"}`}>
                  <Icon className="w-5 h-5" />
                  <div><div className="font-medium text-sm">{t.name}</div><div className="text-xs opacity-70">{t.desc}</div></div>
                </button>
              );
            })}
          </div>
        </aside>

        <main className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl flex flex-col overflow-hidden">
          <div className={`p-4 border-b border-white/10 bg-gradient-to-r ${currentTool.color}`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <currentTool.icon className="w-7 h-7" />
                <div><h1 className="font-bold text-xl">{currentTool.name}</h1><p className="text-sm opacity-80">{currentTool.desc}</p></div>
              </div>
              <button onClick={clear} className="p-2 hover:bg-white/10 rounded-lg"><Trash2 className="w-5 h-5" /></button>
            </div>
          </div>

          <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[85%] rounded-2xl p-4 ${m.role === "user" ? "bg-gradient-to-r from-purple-600 to-pink-600" : "bg-white/10 border border-white/10"}`}>
                  <div className="whitespace-pre-wrap text-sm leading-relaxed">{m.content}</div>
                  {m.role === "assistant" && <button onClick={() => copy(m.content, i)} className="mt-2 text-xs opacity-60 hover:opacity-100">{copiedIdx === i ? "✓ Nusxalandi" : "📋 Nusxalash"}</button>}
                </div>
              </div>
            ))}
            {loading && <div className="flex justify-start"><div className="bg-white/10 rounded-2xl p-4 flex items-center gap-2"><Loader2 className="w-4 h-4 animate-spin" /><span className="text-sm">Yozilmoqda...</span></div></div>}
          </div>

          <div className="p-4 border-t border-white/10">
            <div className="flex items-end gap-2">
              <button className="p-3 hover:bg-white/10 rounded-xl"><Paperclip className="w-5 h-5" /></button>
              <button className="p-3 hover:bg-white/10 rounded-xl"><Mic className="w-5 h-5" /></button>
              <textarea value={input} onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); } }}
                placeholder={`${currentTool.name} uchun savol yozing...`} rows={1}
                className="flex-1 px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-purple-500 focus:outline-none resize-none max-h-32" />
              <button onClick={send} disabled={loading || !input.trim()} className="p-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl disabled:opacity-50"><Send className="w-5 h-5" /></button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
