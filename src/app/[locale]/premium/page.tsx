"use client";
import { useState } from "react";
import { Crown, Check, Sparkles, Award, Zap, Heart, CreditCard, Wallet } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function PremiumPage() {
  const [selectedPlan, setSelectedPlan] = useState("month");
  const [selectedMethod, setSelectedMethod] = useState("payme");
  const [loading, setLoading] = useState(false);

  const plans = [
    { id: "month", name: "1 oy", price: 49000, days: 30, badge: "", save: 0 },
    { id: "year", name: "1 yil", price: 490000, days: 365, badge: "Popular", save: 20 },
    { id: "lifetime", name: "Umrbod", price: 1999000, days: 36500, badge: "Best", save: 60 }
  ];

  const methods = [
    { id: "payme", name: "Payme", icon: "💳" },
    { id: "click", name: "Click", icon: "📱" },
    { id: "uzum", name: "Uzum", icon: "💰" },
    { id: "stripe", name: "Visa/Master", icon: "💎" },
    { id: "ton", name: "TON", icon: "🪙" }
  ];

  const features = [
    { icon: Sparkles, title: "Limitsiz AI", desc: "Barcha 30+ vosita cheklovsiz" },
    { icon: Award, title: "Verified badge", desc: "Profilingizda ko'k belgi" },
    { icon: Zap, title: "Featured", desc: "Startap va xizmatlaringiz tepada" },
    { icon: Heart, title: "Prioritet ko'rish", desc: "Yangi AI funksiyalar birinchi sizda" }
  ];

  const subscribe = async () => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    setLoading(true);
    const plan = plans.find(p => p.id === selectedPlan);
    try {
      const r = await fetch(`${API_URL}/api/v1/payments/create`, {
        method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" },
        body: JSON.stringify({ amount: plan.price, currency: "UZS", method: selectedMethod, description: `Premium ${plan.name}` })
      });
      const d = await r.json();
      if (d.url) window.open(d.url, "_blank");
      else if (d.address) alert(`TON manzil: ${d.address}\nMiqdor: ${plan.price} UZS\nIzoh: ${d.comment}`);
    } catch { alert("Xatolik"); }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-yellow-900 to-slate-900 text-white p-4 md:p-8">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-10">
          <div className="inline-block p-4 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-3xl mb-4">
            <Crown className="w-12 h-12" />
          </div>
          <h1 className="text-5xl font-extrabold mb-3 bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">Premium</h1>
          <p className="text-xl text-gray-300">Barcha imkoniyatlardan foydalaning</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-10">
          {features.map((f, i) => { const Icon = f.icon; return (
            <div key={i} className="bg-white/5 backdrop-blur border border-white/10 rounded-2xl p-4 text-center">
              <div className="w-10 h-10 mx-auto mb-2 rounded-xl bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center"><Icon className="w-5 h-5" /></div>
              <div className="font-semibold text-sm">{f.title}</div>
              <div className="text-xs text-gray-400 mt-1">{f.desc}</div>
            </div>
          );})}
        </div>

        <h2 className="text-2xl font-bold mb-4 text-center">Tarifni tanlang</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          {plans.map(p => (
            <div key={p.id} onClick={() => setSelectedPlan(p.id)}
              className={`relative bg-white/5 backdrop-blur-xl border-2 rounded-2xl p-6 cursor-pointer transition ${selectedPlan === p.id ? "border-yellow-500 scale-105" : "border-white/10 hover:border-white/30"}`}>
              {p.badge && <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full text-xs font-bold">{p.badge}</div>}
              <div className="text-xl font-bold mb-1">{p.name}</div>
              <div className="text-4xl font-extrabold mb-2">{p.price.toLocaleString()}<span className="text-base font-normal text-gray-400"> so'm</span></div>
              {p.save > 0 && <div className="text-sm text-green-400 mb-2">-{p.save}% tejash</div>}
              <ul className="space-y-1 text-sm text-gray-300">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-400" /> Limitsiz AI</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-400" /> Premium badge</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-400" /> Reklama yo'q</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-green-400" /> Prioritet support</li>
              </ul>
            </div>
          ))}
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-6">
          <h3 className="text-lg font-bold mb-3">To'lov usulini tanlang</h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-5">
            {methods.map(m => (
              <div key={m.id} onClick={() => setSelectedMethod(m.id)}
                className={`p-3 rounded-xl border-2 cursor-pointer text-center transition ${selectedMethod === m.id ? "border-yellow-500 bg-yellow-500/10" : "border-white/10 hover:border-white/30"}`}>
                <div className="text-2xl mb-1">{m.icon}</div>
                <div className="text-sm font-medium">{m.name}</div>
              </div>
            ))}
          </div>
          <button onClick={subscribe} disabled={loading} className="w-full py-4 bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold rounded-xl disabled:opacity-50 flex items-center justify-center gap-2">
            <CreditCard className="w-5 h-5" /> {loading ? "Yuklanmoqda..." : "To'lash"}
          </button>
          <p className="text-xs text-gray-400 text-center mt-3">To'lov xavfsiz. SSL shifrlash. Pul qaytarish 14 kun ichida.</p>
        </div>
      </div>
    </div>
  );
}
