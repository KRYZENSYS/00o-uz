"use client";
import { useState, useEffect, useRef } from "react";
import { Send, Paperclip, Smile, Phone, Video, MoreVertical, Search, Plus, Mic, Image as ImageIcon, X } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export default function ChatPage() {
  const [chats, setChats] = useState<any[]>([]);
  const [active, setActive] = useState<any>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [search, setSearch] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => { load(); }, []);

  useEffect(() => {
    if (active) {
      const t = localStorage.getItem("token");
      loadMessages();
      const sock = new WebSocket(`${WS_URL}/api/v1/ws/${active.id}?token=${t}`);
      sock.onopen = () => console.log("WS connected");
      sock.onmessage = (e) => { const m = JSON.parse(e.data); if (m.type === "message") setMessages(p => [...p, m.data]); };
      sock.onclose = () => console.log("WS closed");
      setWs(sock);
      return () => sock.close();
    }
  }, [active]);

  useEffect(() => { scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" }); }, [messages]);

  const load = async () => {
    const t = localStorage.getItem("token");
    try { const r = await fetch(`${API_URL}/api/v1/chat/`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setChats(await r.json()); } catch {}
  };

  const loadMessages = async () => {
    if (!active) return;
    const t = localStorage.getItem("token");
    try { const r = await fetch(`${API_URL}/api/v1/chat/${active.id}/messages`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setMessages(await r.json()); } catch {}
  };

  const send = async () => {
    if (!input.trim() || !active) return;
    const t = localStorage.getItem("token");
    const r = await fetch(`${API_URL}/api/v1/chat/${active.id}/messages`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ content: input, type: "text" }) });
    if (r.ok) { const m = await r.json(); setMessages(p => [...p, m]); setInput(""); }
  };

  const filtered = chats.filter(c => c.name?.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white flex">
      {/* Sidebar */}
      <div className={`w-full md:w-80 bg-black/20 backdrop-blur-xl border-r border-white/10 flex flex-col ${active ? "hidden md:flex" : "flex"}`}>
        <div className="p-4 border-b border-white/10">
          <h1 className="text-2xl font-bold mb-3">💬 Chat</h1>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Qidirish..." className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-full text-sm" />
          </div>
        </div>
        <div className="flex-1 overflow-y-auto">
          {filtered.length === 0 ? <div className="text-center py-20 text-gray-400"><p>Hozircha chat yo'q</p></div> :
            filtered.map(c => (
              <div key={c.id} onClick={() => setActive(c)} className={`p-3 border-b border-white/5 hover:bg-white/5 cursor-pointer flex items-center gap-3 ${active?.id === c.id ? "bg-blue-500/20" : ""}`}>
                <div className="relative">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center font-bold">{c.name?.[0] || c.other_user?.full_name?.[0] || "?"}</div>
                  {c.online && <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-slate-900"></div>}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <div className="font-medium truncate">{c.name || c.other_user?.full_name}</div>
                    {c.last_message && <div className="text-xs text-gray-400">{new Date(c.last_message.created_at).toLocaleTimeString().slice(0, 5)}</div>}
                  </div>
                  <div className="text-sm text-gray-400 truncate">{c.last_message?.content || "Yangi chat"}</div>
                </div>
                {c.unread_count > 0 && <div className="w-5 h-5 bg-blue-500 rounded-full text-xs flex items-center justify-center">{c.unread_count}</div>}
              </div>
            ))}
        </div>
      </div>

      {/* Chat window */}
      <div className={`flex-1 flex flex-col ${!active ? "hidden md:flex" : "flex"}`}>
        {!active ? (
          <div className="flex-1 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <div className="text-6xl mb-4">💬</div>
              <p>Chat tanlang yoki yangi boshlash uchun + bosing</p>
            </div>
          </div>
        ) : (
          <>
            <div className="p-4 border-b border-white/10 flex items-center gap-3">
              <button onClick={() => setActive(null)} className="md:hidden p-1"><X className="w-5 h-5" /></button>
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center font-bold">{active.name?.[0] || active.other_user?.full_name?.[0]}</div>
              <div className="flex-1">
                <div className="font-bold">{active.name || active.other_user?.full_name}</div>
                <div className="text-xs text-green-400">{active.online ? "online" : "offline"}</div>
              </div>
              <button className="p-2 hover:bg-white/10 rounded-lg"><Phone className="w-5 h-5" /></button>
              <button className="p-2 hover:bg-white/10 rounded-lg"><Video className="w-5 h-5" /></button>
              <button className="p-2 hover:bg-white/10 rounded-lg"><MoreVertical className="w-5 h-5" /></button>
            </div>
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-2">
              {messages.length === 0 ? <div className="text-center py-20 text-gray-400">Birinchi xabarni yozing!</div> :
                messages.map((m: any) => (
                  <div key={m.id} className={`flex ${m.is_mine ? "justify-end" : "justify-start"}`}>
                    <div className={`max-w-[70%] px-4 py-2 rounded-2xl ${m.is_mine ? "bg-blue-500" : "bg-white/10"}`}>
                      {m.content}
                      <div className={`text-xs mt-1 ${m.is_mine ? "text-blue-100" : "text-gray-400"}`}>{new Date(m.created_at).toLocaleTimeString().slice(0, 5)}</div>
                    </div>
                  </div>
                ))}
            </div>
            <div className="p-3 border-t border-white/10 flex items-center gap-2">
              <button className="p-2 hover:bg-white/10 rounded-full"><Paperclip className="w-5 h-5" /></button>
              <button className="p-2 hover:bg-white/10 rounded-full"><ImageIcon className="w-5 h-5" /></button>
              <input value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={(e) => e.key === "Enter" && send()} placeholder="Xabar yozing..." className="flex-1 px-4 py-2 bg-white/5 border border-white/10 rounded-full text-sm" />
              <button className="p-2 hover:bg-white/10 rounded-full"><Mic className="w-5 h-5" /></button>
              <button onClick={send} className="p-2 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"><Send className="w-5 h-5" /></button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
