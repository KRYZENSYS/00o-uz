"use client";
import Link from "next/link";
import { Rocket, Sparkles, Briefcase, Wrench, TrendingUp, Users, Award, ArrowRight, Check } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      <section className="relative overflow-hidden pt-20 pb-32 px-4">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500 rounded-full filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute top-40 right-10 w-96 h-96 bg-pink-500 rounded-full filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="relative max-w-6xl mx-auto text-center">
          <div className="inline-block mb-4 px-4 py-1.5 bg-white/5 border border-white/10 rounded-full text-sm text-purple-300">🇺🇿 O'zbekistondagi #1 AI platforma</div>
          <h1 className="text-5xl md:text-7xl font-extrabold mb-6 leading-tight">Kelajak <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-yellow-400 bg-clip-text text-transparent">AI</span> bilan bugun</h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">30+ AI vosita, startaplar, ish o'rinlari, freelance xizmatlar — barchasi bir joyda</p>
          <div className="flex flex-wrap items-center justify-center gap-4">
            <Link href="/ai" className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl font-bold text-lg hover:shadow-2xl hover:shadow-purple-500/50 flex items-center gap-2">
              <Sparkles className="w-5 h-5" /> AI bilan boshlash <ArrowRight className="w-5 h-5" />
            </Link>
            <Link href="/startups" className="px-8 py-4 bg-white/10 border border-white/20 rounded-2xl font-bold text-lg">Startaplar</Link>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-16 max-w-3xl mx-auto">
            {[{ v: "10K+", l: "Foydalanuvchi" }, { v: "500+", l: "Startup" }, { v: "1000+", l: "Ish o'rni" }, { v: "30+", l: "AI vosita" }].map((s, i) => (
              <div key={i} className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-4">
                <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">{s.v}</div>
                <div className="text-sm text-gray-400">{s.l}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-12">Imkoniyatlar</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: Sparkles, title: "AI Yordamchi", desc: "30+ vosita", color: "from-purple-500 to-pink-500", href: "/ai" },
              { icon: Rocket, title: "Startaplar", desc: "G'oyalar va investitsiyalar", color: "from-blue-500 to-cyan-500", href: "/startups" },
              { icon: Briefcase, title: "Ish o'rinlari", desc: "Vakansiyalar", color: "from-green-500 to-emerald-500", href: "/jobs" },
              { icon: Wrench, title: "Freelance", desc: "Xizmatlar", color: "from-yellow-500 to-orange-500", href: "/services" },
              { icon: Users, title: "Jamoa", desc: "Hamkor topish", color: "from-red-500 to-pink-500", href: "/team" },
              { icon: TrendingUp, title: "Investorlar", desc: "Moliya topish", color: "from-indigo-500 to-purple-500", href: "/investors" },
            ].map((f, i) => { const Icon = f.icon; return (
              <Link key={i} href={f.href} className="group bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-6 hover:border-white/30 hover:scale-105 transition">
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${f.color} flex items-center justify-center mb-4`}><Icon className="w-7 h-7" /></div>
                <h3 className="text-xl font-bold mb-2">{f.title}</h3>
                <p className="text-gray-400 text-sm">{f.desc}</p>
              </Link>
            );})}
          </div>
        </div>
      </section>

      <section className="py-20 px-4 bg-black/20">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-center mb-12">🤖 30+ AI vosita</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
            {["💼 Biznes reja", "🎯 Pitch deck", "💡 G'oyalar", "💻 Kod", "🌍 Tarjimon", "📄 Resume", "📊 Marketing", "🔍 SEO", "✍️ Blog", "📋 Xulosa", "🐛 Bug fix", "📧 Email"].map((t, i) => (
              <div key={i} className="bg-white/5 border border-white/10 rounded-xl p-3 text-center text-sm hover:bg-white/10 cursor-pointer">{t}</div>
            ))}
          </div>
          <div className="text-center mt-8"><Link href="/ai" className="inline-block px-8 py-3 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl font-bold">Barchasi →</Link></div>
        </div>
      </section>

      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto bg-gradient-to-br from-purple-600 to-pink-600 rounded-3xl p-8 md:p-12">
          <Award className="w-12 h-12 mb-4" />
          <h2 className="text-4xl md:text-5xl font-bold mb-4">💎 Premium</h2>
          <p className="text-xl mb-6">AI limitsiz + barcha premium imkoniyatlar</p>
          <div className="grid md:grid-cols-2 gap-2 mb-6">
            {["Limitsiz AI", "Featured", "Verified badge", "Reklama yo'q", "Prioritet support", "Early access"].map((f, i) => (
              <div key={i} className="flex items-center gap-2"><Check className="w-5 h-5" />{f}</div>
            ))}
          </div>
          <div className="flex items-end gap-4">
            <div className="text-4xl font-bold">49,000 so'm<span className="text-lg font-normal">/oy</span></div>
            <Link href="/premium" className="px-8 py-3 bg-white text-purple-900 rounded-xl font-bold">Premium olish</Link>
          </div>
        </div>
      </section>
    </div>
  );
}
