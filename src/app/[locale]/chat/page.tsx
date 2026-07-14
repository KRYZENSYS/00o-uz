"use client";
import { useState, useEffect, useRef } from "react";
import { MessageCircle, Send, Search, ArrowLeft, Phone, Video, MoreVertical, Smile, Paperclip, Check, CheckCheck } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/api/v1/ws";

export default function ChatPage() {
  const [chats, setChats] = useState<any[]>([]);
  const [active, setActive] = useState<any>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(true);
  const [online, setOnline] = useState<any>({});
  const [typing, setTyping] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEnd = useRef<HTMLDivElement>(null);

  useEffect(() => { loadChats(); connectWS(); }, []);

  useEffect(() => { if (active) loadMessages(); }, [active]);

  useEffect(() => { messagesEnd.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const connectWS = () => {
    const t = localStorage.getItem("token");
    if (!t) return;
    const userId = JSON.parse(localStorage.getItem("user") || "{}").id;
    const ws = new WebSocket(`${WS_URL}/${userId}`);
    ws.onmessage = (e) => {
      const d = JSON.parse(e.data);
      if (d.type === "new_message" && d.chat_id === active?.id) {
        setMessages(prev => [...prev, d.message]);
      } else if (d.type === "typing" && d.from === active?.other_user.id) {
        setTyping(true); setTimeout(() => setTyping(false), 2000);
      }
    };
    wsRef.current = ws;
  };

  const loadChats = async () => {
    const t = localStorage.getItem("token");
    try {
      const r = await fetch(`${API_URL}/api/v1/chat/`, { headers: { Authorization: `Bearer ${t}` }});
      if (r.ok) {
        const data = await r.json();
        setChats(data);
        data.forEach((c: any) => setOnline(prev => ({ ...prev, [c.other_user.id]: c.other_user.is_online })));
      }
    } catch {}
    setLoading(false);
  };

  const loadMessages = async () => {
    const t = localStorage.getItem("token");
    const r = await fetch(`${API_URL}/api/v1/chat/${active.id}/messages`, { headers: { Authorization: `Bearer ${t}` }});
    if (r.ok) setMessages(await r.json());
    // Mark as read
    await fetch(`${API_URL}/api/v1/chat/${active.id}/read`, { method: "POST", headers: { Authorization: `Bearer ${t}` }});
  };

  const send = async () => {
    if (!input.trim() || !active) return;
    const t = localStorage.getItem("token");
    const content = input;
    setInput("");
    
    // Optimistic
    const tempMsg = { id: Date.now(), content, sender_id: JSON.parse(localStorage.getItem("user") || "{}").id, is_mine: true, created_at: new Date().toISOString() };
    setMessages(prev => [...prev, tempMsg]);
    
    await fetch(`${API_URL}/api/v1/chat/${active.id}/messages`, {
      method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" },
      body: JSON.stringify({ content, type: "text" })
    });
  };

  const sendTyping = () => {
    if (active && wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({ type: "typing", to: active.other_user.id }));
    }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white"><div className="w-12 h-12 border-4 border-pink-500 border-t-transparent rounded-full animate-spin"></div></div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-pink-900 to-slate-900 text-white flex">
      <div className={`${active ? "hidden md:flex" : "flex"} w-full md:w-80 flex-col bg-black/20 backdrop-blur border-r border-white/10`}>
        <div className="p-4 border-b border-white/10">
          <h1 className="text-2xl font-bold flex items-center gap-2"><MessageCircle className="w-6 h-6" /> Chatlar</h1>
          <div className="mt-3 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input placeholder="Qidirish..." className="w-full pl-9 pr-3 py-2 bg-white/5 border border-white/10 rounded-lg text-sm" />
          </div>
        </div>
        <div className="flex-1 overflow-y-auto">
          {chats.length === 0 ? (
            <div className="p-8 text-center text-gray-400">
              <MessageCircle className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p>Hali chatlar yo'q</p>
            </div>
          ) : chats.map(c => (
            <div key={c.id} onClick={() => setActive(c)} className={`p-3 hover:bg-white/5 cursor-pointer flex items-center gap-3 ${active?.id === c.id ? "bg-white/10" : ""}`}>
              <div className="relative">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-pink-500 to-purple-500 flex items-center justify-center font-bold">{c.other_user.full_name?.[0]}</div>
                {online[c.other_user.id] && <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-slate-900" />}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <div className="font-medium truncate">{c.other_user.full_name}</div>
                  <div className="text-xs text-gray-400">{c.last_message && new Date(c.last_message.created_at).toLocaleTimeString().slice(0, 5)}</div>
                </div>
                <div className="text-sm text-gray-400 truncate">{c.last_message?.content || "Yangi chat"}</div>
              </div>
              {c.unread_count > 0 && <div className="w-5 h-5 bg-pink-500 rounded-full text-xs flex items-center justify-center">{c.unread_count}</div>}
            </div>
          ))}
        </div>
      </div>

      {active ? (
        <div className="flex-1 flex flex-col">
          <div className="p-4 border-b border-white/10 bg-black/20 backdrop-blur flex items-center gap-3">
            <button onClick={() => setActive(null)} className="md:hidden"><ArrowLeft className="w-5 h-5" /></button>
            <div className="relative">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-pink-500 to-purple-500 flex items-center justify-center font-bold">{active.other_user.full_name?.[0]}</div>
              {online[active.other_user.id] && <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-slate-900" />}
            </div>
            <div className="flex-1">
              <div className="font-semibold">{active.other_user.full_name}</div>
              <div className="text-xs text-gray-400">{typing ? "yozmoqda..." : online[active.other_user.id] ? "onlayn" : "offlayn"}</div>
            </div>
            <button className="p-2 hover:bg-white/10 rounded-lg"><Phone className="w-5 h-5" /></button>
            <button className="p-2 hover:bg-white/10 rounded-lg"><Video className="w-5 h-5" /></button>
            <button className="p-2 hover:bg-white/10 rounded-lg"><MoreVertical className="w-5 h-5" /></button>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map(m => (
              <div key={m.id} className={`flex ${m.is_mine ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[70%] px-4 py-2 rounded-2xl ${m.is_mine ? "bg-gradient-to-r from-pink-500 to-purple-500" : "bg-white/10"}`}>
                  <p>{m.content}</p>
                  <div className="flex items-center gap-1 justify-end mt-1 text-xs opacity-70">
                    {new Date(m.created_at).toLocaleTimeString().slice(0, 5)}
                    {m.is_mine && (m.is_read ? <CheckCheck className="w-3 h-3" /> : <Check className="w-3 h-3" />)}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEnd} />
          </div>
          
          <div className="p-4 border-t border-white/10 bg-black/20 backdrop-blur flex items-center gap-2">
            <button className="p-2 hover:bg-white/10 rounded-lg"><Paperclip className="w-5 h-5" /></button>
            <button className="p-2 hover:bg-white/10 rounded-lg"><Smile className="w-5 h-5" /></button>
            <input value={input} onChange={(e) => { setInput(e.target.value); sendTyping(); }}
              onKeyDown={(e) => e.key === "Enter" && send()} placeholder="Xabar yozing..."
              className="flex-1 px-4 py-2 bg-white/5 border border-white/10 rounded-full focus:outline-none focus:border-pink-500" />
            <button onClick={send} className="p-2 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full"><Send className="w-5 h-5" /></button>
          </div>
        </div>
      ) : (
        <div className="hidden md:flex flex-1 items-center justify-center text-gray-400">
          <div className="text-center"><MessageCircle className="w-16 h-16 mx-auto mb-2 opacity-50" /><p>Chatni tanlang</p></div>
        </div>
      )}
    </div>
  );
}
