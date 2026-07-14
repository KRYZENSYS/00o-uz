"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { Mail, Lock, Loader2, Send, Sparkles } from "lucide-react";
import Link from "next/link";

export default function LoginPage() {
  const t = useTranslations("auth");
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Login failed");
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      router.push("/dashboard");
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTelegram = async () => {
    // Telegram OAuth redirect
    const tg = (window as any).Telegram?.Login;
    if (tg) {
      tg({ bot_id: process.env.NEXT_PUBLIC_TELEGRAM_BOT_ID, request_access: true }, async (data: any) => {
        if (data) {
          const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/telegram`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
          });
          const result = await res.json();
          localStorage.setItem("access_token", result.access_token);
          router.push("/dashboard");
        }
      });
    } else {
      window.location.href = "https://t.me/00o_uz_bot?start=login";
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-500/20 rounded-full blur-3xl" />
      </div>
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center glow">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-2xl font-bold gradient-text">00o.uz</span>
          </div>
          <h1 className="text-2xl font-bold">{t("signInTitle")}</h1>
        </div>

        <div className="glass-strong rounded-2xl p-8 space-y-4">
          {error && (
            <div className="px-4 py-3 rounded-lg bg-red-500/20 text-red-400 text-sm">{error}</div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="text-sm text-gray-400 mb-1 block">{t("email")}</label>
              <div className="relative">
                <Mail className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-3 py-3 rounded-xl glass outline-none focus:bg-white/10" required />
              </div>
            </div>
            <div>
              <label className="text-sm text-gray-400 mb-1 block">{t("password")}</label>
              <div className="relative">
                <Lock className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-3 py-3 rounded-xl glass outline-none focus:bg-white/10" required />
              </div>
            </div>
            <button type="submit" disabled={loading}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 font-medium disabled:opacity-50">
              {loading ? <Loader2 className="w-4 h-4 animate-spin mx-auto" /> : t("signIn")}
            </button>
          </form>

          <div className="relative my-4">
            <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-white/10"></div></div>
            <div className="relative flex justify-center text-xs"><span className="bg-slate-950 px-2 text-gray-400">yoki</span></div>
          </div>

          <button onClick={handleTelegram}
            className="w-full py-3 rounded-xl glass hover:bg-white/10 transition flex items-center justify-center gap-2">
            <Send className="w-4 h-4" /> {t("signInWithTelegram")}
          </button>

          <p className="text-center text-sm text-gray-400 pt-2">
            {t("dontHaveAccount")} <Link href="/register" className="text-purple-400 hover:underline">{t("signUp")}</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
