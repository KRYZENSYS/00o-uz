"use client";
import { useState, useEffect } from "react";
import { Sparkles, TrendingUp, Users, Rocket, Briefcase, Wrench, GraduationCap, DollarSign, Trophy, MessageCircle, Bell, Search, Menu, X, ChevronRight, Crown, Heart, Eye, Star, Zap, Globe, BookOpen, BarChart3, Target, Mic, Image as ImageIcon, Video } from "lucide-react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function HomePage() {
  const [stats, setStats] = useState({ users: 12500, startups: 3500, jobs: 1200, services: 4800, courses: 280, ai_requests: 125000 });
  const [menuOpen, setMenuOpen] = useState(false);

  const categories = [
    { icon: Rocket, name: "Startaplar", count: stats.startups, color: "from-purple-500 to-pink-500", href: "/startups" },
    { icon: Briefcase, name: "Ish o'rinlari", count: stats.jobs, color: "from-blue-500 to-cyan-500", href: "/jobs" },
    { icon: Wrench, name: "Xizmatlar", count: stats.services, color: "from-green-500 to-emerald-500", href: "/services" },
    { icon: GraduationCap, name: "Kurslar", count: stats.courses, color: "from-yellow-500 to-orange-500", href: "/courses" },
    { icon: DollarSign, name: "Investorlar", count: 240, color: "from-emerald-500 to-green-500", href: "/investors" },
    { icon: Users, name: "Jamoalar", count: 890, color: "from-rose-500 to-pink-500", href: "/teams" },
    { icon: MessageCircle, name: "Chat", count: "∞", color: "from-indigo-500 to-purple-500", href: "/chat" },
    { icon: Trophy, name: "Game", count: "XP", color: "from-amber-500 to-yellow-500", href: "/game" },
    { icon: BookOpen, name: "Blog", count: 156, color: "from-pink-500 to-rose-500", href: "/blog" },
    { icon: Globe, name: "Community", count: 320, color: "from-teal-500 to-cyan-500", href: "/community" },
    { icon: Video, name: "Live", count: 12, color: "from-red-500 to-pink-500", href: "/live" },
    { icon: ImageIcon, name: "Market", count: 890, color: "from-orange-500 to-red-500", href: "/market" },
  ];

  const aiTools = [
    { icon: Sparkles, name: "AI Chat", color: "from-purple-500 to-pink-500", href: "/ai?tool=chat" },
    { icon: Briefcase, name: "Biznes reja", color: "from-blue-500 to-cyan-500", href: "/ai?tool=business-plan" },
    { icon: Target, name: "Pitch deck", color: "from-green-500 to-emerald-500", href: "/ai?tool=pitch-deck" },
    { icon: BarChart3, name: "SWOT", color: "from-orange-500 to-red-500", href: "/ai?tool=swot" },
    { icon: ImageIcon, name: "Rasm yaratish", color: "from-violet-500 to-purple-500", href: "/game" },
    { icon: Mic, name: "Ovoz", color: "from-pink-500 to-rose-500", href: "/game" },
    { icon: Globe, name: "Tarjimon", color: "from-cyan-500 to-blue-500", href: "/ai?tool=translate" },
    { icon: CodeIcon, name: "Kod", color: "from-slate-500 to-slate-700", href: "/ai?tool=code" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      {/* Header */}
      <header className="sticky top-0 z-30 bg-slate-900/80 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-3">
          <div className="text-2xl font-extrabold bg-gradient-to-r from-purple-400 via-pink-400 to-orange-400 bg-clip-text text-transparent">00o.uz</div>
          <div className="flex-1 max-w-md hidden md:block">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input placeholder="Qidirish..." className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-full text-sm" />
            </div>
          </div>
          <button className="p-2 hover:bg-white/10 rounded-full relative">
            <Bell className="w-5 h-5" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          <Link href="/premium" className="hidden md:flex items-center gap-1 px-3 py-1.5 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full text-sm font-medium text-black">
            <Crown className="w-4 h-4" /> Premium
          </Link>
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center font-bold">U</div>
          <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden p-2">{menuOpen ? <X /> : <Menu />}</button>
        </div>
        {menuOpen && (
          <div className="md:hidden bg-slate-900 border-t border-white/10 p-4 space-y-2">
            {categories.map(c => (
              <Link key={c.name} href={c.href} className="flex items-center gap-2 p-2 rounded-lg hover:bg-white/5" onClick={() => setMenuOpen(false)}>
                <c.icon className="w-4 h-4" /> {c.name}
              </Link>
            ))}
          </div>
        )}
      </header>

      {/* Hero */}
      <section className="px-4 py-12 text-center">
        <div className="max-w-4xl mx-auto">
          <div className="inline-block mb-4">
            <span className="px-4 py-1.5 bg-white/10 backdrop-blur rounded-full text-sm">🇺🇿 O'zbekistondagi #1 AI platforma</span>
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold mb-4 bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent leading-tight">
            Kelajak AI bilan bugun
          </h1>
          <p className="text-lg text-gray-300 mb-8 max-w-2xl mx-auto">
            30+ AI vosita, 12,500+ foydalanuvchi, 3,500+ startap. Startapchilar, frilanserlar, investorlar va talabalar uchun yagona platforma.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-3">
            <Link href="/ai" className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full font-bold flex items-center gap-2">
              <Sparkles className="w-5 h-5" /> AI bilan boshlash
            </Link>
            <Link href="/startups" className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-full font-medium flex items-center gap-2">
              Startaplarni ko'rish <ChevronRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="px-4 pb-8">
        <div className="max-w-6xl mx-auto grid grid-cols-2 md:grid-cols-5 gap-3">
          {[
            { l: "Foydalanuvchi", v: stats.users.toLocaleString(), i: Users, c: "from-blue-500 to-cyan-500" },
            { l: "Startap", v: stats.startups.toLocaleString(), i: Rocket, c: "from-purple-500 to-pink-500" },
            { l: "Ish", v: stats.jobs.toLocaleString(), i: Briefcase, c: "from-green-500 to-emerald-500" },
            { l: "AI so'rov", v: stats.ai_requests.toLocaleString(), i: Sparkles, c: "from-yellow-500 to-orange-500" },
            { l: "Premium", v: "1,200+", i: Crown, c: "from-amber-400 to-yellow-500" },
          ].map((s, i) => { const Icon = s.i; return (
            <div key={i} className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-3 text-center">
              <div className={`w-10 h-10 mx-auto rounded-xl bg-gradient-to-br ${s.c} flex items-center justify-center mb-2`}><Icon className="w-5 h-5" /></div>
              <div className="text-xl font-bold">{s.v}</div>
              <div className="text-xs text-gray-400">{s.l}</div>
            </div>
          );})}
        </div>
      </section>

      {/* Categories */}
      <section className="px-4 pb-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold mb-4 flex items-center gap-2"><Globe className="w-6 h-6 text-purple-400" /> Platformalar</h2>
          <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
            {categories.map((c, i) => { const Icon = c.icon; return (
              <Link key={i} href={c.href} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 hover:border-purple-500/50 transition text-center group">
                <div className={`w-12 h-12 mx-auto rounded-xl bg-gradient-to-br ${c.color} flex items-center justify-center mb-2 group-hover:scale-110 transition`}><Icon className="w-6 h-6" /></div>
                <div className="font-medium text-sm">{c.name}</div>
                <div className="text-xs text-gray-400">{c.count.toLocaleString()}</div>
              </Link>
            );})}
          </div>
        </div>
      </section>

      {/* AI Tools */}
      <section className="px-4 pb-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl font-bold mb-4 flex items-center gap-2"><Sparkles className="w-6 h-6 text-purple-400" /> AI vositalar (30+)</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {aiTools.map((t, i) => { const Icon = t.icon; return (
              <Link key={i} href={t.href} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 hover:scale-105 transition">
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${t.color} flex items-center justify-center mb-2`}><Icon className="w-5 h-5" /></div>
                <div className="font-medium">{t.name}</div>
              </Link>
            );})}
          </div>
        </div>
      </section>

      {/* Premium CTA */}
      <section className="px-4 pb-12">
        <div className="max-w-4xl mx-auto bg-gradient-to-br from-yellow-500/20 to-orange-500/20 border border-yellow-500/30 rounded-3xl p-8 text-center">
          <Crown className="w-16 h-16 mx-auto mb-3 text-yellow-400" />
          <h2 className="text-3xl font-bold mb-2">Premium ga o'ting</h2>
          <p className="text-gray-300 mb-5">Limitsiz AI, verified badge, featured listings, reklama yo'q</p>
          <div className="flex flex-wrap items-center justify-center gap-3">
            <div className="px-4 py-2 bg-white/10 rounded-full text-sm">1 oy: 49,000 so'm</div>
            <div className="px-4 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-black rounded-full text-sm font-bold">1 yil: 490,000 so'm (-20%)</div>
            <div className="px-4 py-2 bg-white/10 rounded-full text-sm">Umrbod: 1,999,000 so'm (-60%)</div>
          </div>
          <Link href="/premium" className="inline-block mt-5 px-8 py-3 bg-gradient-to-r from-yellow-500 to-orange-500 text-black rounded-full font-bold">
            Premium olish
          </Link>
        </div>
      </section>
    </div>
  );
}

function CodeIcon(props: any) { return <svg {...props} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="16 18 22 12 16 6" /><polyline points="8 6 2 12 8 18" /></svg>; }
