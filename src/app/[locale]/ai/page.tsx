"use client";
import { useState } from "react";
import { Sparkles, Send, Loader2, Code, Lightbulb, BarChart, Languages, FileText, Rocket } from "lucide-react";
import { useTranslations } from "next-intl";

export default function AIPage() {
  const t = useTranslations("ai");
  const [messages, setMessages] = useState<{ role: "user" | "ai"; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [tool, setTool] = useState("chat");

  const tools = [
    { id: "chat", icon: Sparkles, label: "AI Chat" },
    { id: "startup-ideas", icon: Lightbulb, label: "Startup Ideas" },
    { id: "business-plan", icon: FileText, label: "Business Plan" },
    { id: "analyze", icon: BarChart, label: "Analyzer" },
    { id: "translate", icon: Languages, label: "Translator" },
    { id: "summarize", icon: FileText, label: "Summarizer" },
    { id: "code", icon: Code, label: "Code Gen" },
  ];

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg = { role: "user" as const, content: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      const endpoint = tool === "chat" ? "chat" : tool;
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/ai/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          input: userMsg.content,
          language: localStorage.getItem("locale") || "uz"
        }),
      });
      const data = await res.json();
      setMessages((m) => [...m, { role: "ai", content: data.content || data.error || "Xatolik" }]);
    } catch (e) {
      setMessages((m) => [...m, { role: "ai", content: "Tarmoq xatosi. Iltimos qayta urinib ko'ring." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen max-w-7xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-4">
          <Sparkles className="w-4 h-4 text-purple-400" />
          <span className="text-sm">Powered by GroqCloud</span>
        </div>
        <h1 className="text-4xl font-bold gradient-text mb-2">{t("title")}</h1>
        <p className="text-gray-400">{t("subtitle")}</p>
      </div>

      <div className="flex flex-wrap gap-2 mb-6 justify-center">
        {tools.map((tt) => (
          <button key={tt.id} onClick={() => setTool(tt.id)}
            className={`px-4 py-2 rounded-xl flex items-center gap-2 text-sm transition ${
              tool === tt.id ? "bg-gradient-to-r from-purple-500 to-pink-500" : "glass hover:bg-white/10"
            }`}>
            <tt.icon className="w-4 h-4" /> {tt.label}
          </button>
        ))}
      </div>

      <div className="glass-strong rounded-2xl overflow-hidden">
        <div className="h-[500px] overflow-y-auto p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center text-gray-400">
              <Rocket className="w-16 h-16 mb-4 text-purple-400" />
              <p className="text-lg">Savolingizni yozing va AI yordam beradi</p>
            </div>
          ) : (
            messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  m.role === "user" ? "bg-gradient-to-r from-purple-500 to-pink-500" : "glass"
                }`}>
                  <pre className="whitespace-pre-wrap font-sans">{m.content}</pre>
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="flex justify-start">
              <div className="glass rounded-2xl px-4 py-3 flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin" /> {t("thinking")}
              </div>
            </div>
          )}
        </div>
        <div className="border-t border-white/10 p-4 flex gap-2">
          <input value={input} onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder={t("input")}
            className="flex-1 bg-transparent outline-none px-4 py-3 rounded-xl glass" />
          <button onClick={send} disabled={loading || !input.trim()}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 font-medium disabled:opacity-50">
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
