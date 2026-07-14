"use client";
import { useState } from "react";
import { X, Mail, Lock, User, Eye, EyeOff, Phone } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function AuthModal({ onClose, onSuccess }: any) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [form, setForm] = useState({ email: "", phone: "", username: "", full_name: "", password: "" });
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true); setError("");
    try {
      const url = mode === "login" ? "/auth/login" : "/auth/register";
      const body: any = mode === "login" ? { email_or_username: form.email, password: form.password } : form;
      const r = await fetch(`${API_URL}/api/v1${url}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const data = await r.json();
      if (!r.ok) throw new Error(data.detail);
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(data.user));
      onSuccess(data.user); onClose();
    } catch (e: any) { setError(e.message); }
    setLoading(false);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-gradient-to-br from-slate-900 to-purple-900 border border-white/10 rounded-2xl p-6 w-full max-w-md relative">
        <button onClick={onClose} className="absolute top-4 right-4 p-1 hover:bg-white/10 rounded-lg"><X className="w-5 h-5 text-white" /></button>
        <h2 className="text-2xl font-bold text-white mb-2">{mode === "login" ? "Kirish" : "Ro'yxatdan o'tish"}</h2>
        <form onSubmit={submit} className="space-y-3 mt-4">
          {mode === "register" && (
            <>
              <div className="relative"><User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input required placeholder="To'liq ism" value={form.full_name} onChange={(e) => setForm({...form, full_name: e.target.value})} className="w-full pl-10 pr-3 py-3 bg-white/5 border border-white/10 rounded-xl text-white" /></div>
              <div className="relative"><User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input required placeholder="Username" value={form.username} onChange={(e) => setForm({...form, username: e.target.value})} className="w-full pl-10 pr-3 py-3 bg-white/5 border border-white/10 rounded-xl text-white" /></div>
            </>
          )}
          <div className="relative"><Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input required type="email" placeholder="Email" value={form.email} onChange={(e) => setForm({...form, email: e.target.value})} className="w-full pl-10 pr-3 py-3 bg-white/5 border border-white/10 rounded-xl text-white" /></div>
          <div className="relative"><Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input required type={showPass ? "text" : "password"} placeholder="Parol" value={form.password} onChange={(e) => setForm({...form, password: e.target.value})} className="w-full pl-10 pr-10 py-3 bg-white/5 border border-white/10 rounded-xl text-white" />
            <button type="button" onClick={() => setShowPass(!showPass)} className="absolute right-3 top-1/2 -translate-y-1/2">{showPass ? <EyeOff className="w-4 h-4 text-gray-400" /> : <Eye className="w-4 h-4 text-gray-400" />}</button></div>
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button type="submit" disabled={loading} className="w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl font-bold text-white disabled:opacity-50">{loading ? "..." : mode === "login" ? "Kirish" : "Ro'yxatdan o'tish"}</button>
        </form>
        <div className="my-4 flex items-center gap-3"><div className="flex-1 h-px bg-white/10" /><span className="text-gray-500 text-sm">yoki</span><div className="flex-1 h-px bg-white/10" /></div>
        <button onClick={() => window.location.href = "https://t.me/oo0o_uz_bot"} className="w-full py-3 bg-blue-500/20 border border-blue-500/30 rounded-xl text-white">📱 Telegram orqali</button>
        <p className="text-center text-gray-400 text-sm mt-4">{mode === "login" ? "Akkauntingiz yo'qmi?" : "Akkauntingiz bormi?"} <button onClick={() => setMode(mode === "login" ? "register" : "login")} className="text-purple-400">{mode === "login" ? "Ro'yxatdan o'tish" : "Kirish"}</button></p>
      </div>
    </div>
  );
}
