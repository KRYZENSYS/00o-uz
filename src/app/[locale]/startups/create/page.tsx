"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Rocket, Loader2, Sparkles, Wand2 } from "lucide-react";
import Link from "next/link";

export default function CreateStartupPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    name: "", tagline: "", description: "",
    category: "saas", stage: "idea",
    funding_goal: 100000,
  });
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);

  const generateWithAI = async () => {
    if (!form.name) {
      alert("Avval startap nomini kiriting");
      return;
    }
    setAiLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/ai/business-plan`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ input: form.name, language: "uz" }),
      });
      const data = await res.json();
      if (data.content) {
        setForm({ ...form, description: data.content });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setAiLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        router.push("/login");
        return;
      }
      // Backend API yaratilganda shu yerga ulanadi
      alert("✅ Startup yaratildi! (Backend API tayyor bo'lganda saqlanadi)");
      router.push("/startups");
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen max-w-3xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold gradient-text mb-2">Create Startup</h1>
        <p className="text-gray-400">Yangi startap yarating va dunyoga tanishtiring</p>
      </div>

      <form onSubmit={handleSubmit} className="glass-strong rounded-2xl p-8 space-y-6">
        <div>
          <label className="text-sm text-gray-400 mb-2 block">Startup nomi *</label>
          <input value={form.name} onChange={(e) => setForm({...form, name: e.target.value})}
            className="w-full px-4 py-3 rounded-xl glass outline-none" required minLength={2} maxLength={100} />
        </div>

        <div>
          <label className="text-sm text-gray-400 mb-2 block">Tagline (qisqacha)</label>
          <input value={form.tagline} onChange={(e) => setForm({...form, tagline: e.target.value})}
            className="w-full px-4 py-3 rounded-xl glass outline-none" maxLength={200} />
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm text-gray-400">Tavsif</label>
            <button type="button" onClick={generateWithAI} disabled={aiLoading}
              className="text-xs px-3 py-1 rounded-lg bg-gradient-to-r from-purple-500 to-pink-500 flex items-center gap-1">
              {aiLoading ? <Loader2 className="w-3 h-3 animate-spin" /> : <Wand2 className="w-3 h-3" />}
              AI bilan yozish
            </button>
          </div>
          <textarea value={form.description} onChange={(e) => setForm({...form, description: e.target.value})}
            rows={6} className="w-full px-4 py-3 rounded-xl glass outline-none resize-none" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm text-gray-400 mb-2 block">Kategoriya</label>
            <select value={form.category} onChange={(e) => setForm({...form, category: e.target.value})}
              className="w-full px-4 py-3 rounded-xl glass outline-none bg-slate-900">
              <option value="fintech">Fintech</option>
              <option value="edtech">EdTech</option>
              <option value="healthtech">HealthTech</option>
              <option value="agritech">AgriTech</option>
              <option value="saas">SaaS</option>
              <option value="ai">AI</option>
              <option value="ecommerce">Ecommerce</option>
              <option value="other">Boshqa</option>
            </select>
          </div>
          <div>
            <label className="text-sm text-gray-400 mb-2 block">Bosqich</label>
            <select value={form.stage} onChange={(e) => setForm({...form, stage: e.target.value})}
              className="w-full px-4 py-3 rounded-xl glass outline-none bg-slate-900">
              <option value="idea">Idea</option>
              <option value="mvp">MVP</option>
              <option value="early">Early</option>
              <option value="growth">Growth</option>
              <option value="scale">Scale</option>
            </select>
          </div>
        </div>

        <div>
          <label className="text-sm text-gray-400 mb-2 block">Moliyalashtirish maqsadi ($)</label>
          <input type="number" value={form.funding_goal} onChange={(e) => setForm({...form, funding_goal: +e.target.value})}
            className="w-full px-4 py-3 rounded-xl glass outline-none" min={0} />
        </div>

        <div className="flex gap-3 pt-4">
          <button type="submit" disabled={loading}
            className="flex-1 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 font-medium disabled:opacity-50 flex items-center justify-center gap-2">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Rocket className="w-4 h-4" />}
            {loading ? "Yaratilmoqda..." : "Startup yaratish"}
          </button>
          <Link href="/startups"
            className="px-6 py-3 rounded-xl glass hover:bg-white/10 text-center">
            Bekor
          </Link>
        </div>
      </form>
    </div>
  );
}
