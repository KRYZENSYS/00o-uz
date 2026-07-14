"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { LogOut, User as UserIcon, Sparkles, Activity, MessageCircle, Briefcase, Rocket, TrendingUp } from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [stats, setStats] = useState({ startups: 0, services: 0, messages: 0, aiCalls: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/login");
      return;
    }
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then((r) => r.ok ? r.json() : null)
      .then((data) => {
        if (data) setUser(data);
        else router.push("/login");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    router.push("/login");
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-12 h-12 rounded-full border-4 border-purple-500 border-t-transparent animate-spin" />
      </div>
    );
  }

  const cards = [
    { icon: Rocket, label: "My Startups", value: stats.startups, color: "from-purple-500 to-pink-500" },
    { icon: Briefcase, label: "My Services", value: stats.services, color: "from-blue-500 to-cyan-500" },
    { icon: MessageCircle, label: "Messages", value: stats.messages, color: "from-green-500 to-emerald-500" },
    { icon: Sparkles, label: "AI Calls", value: stats.aiCalls, color: "from-orange-500 to-red-500" },
  ];

  return (
    <div className="min-h-screen max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">Welcome, {user?.full_name}!</h1>
          <p className="text-gray-400">{user?.email} · {user?.role}</p>
        </div>
        <button onClick={handleLogout}
          className="px-4 py-2 rounded-xl glass hover:bg-white/10 flex items-center gap-2">
          <LogOut className="w-4 h-4" /> Logout
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {cards.map((c, i) => (
          <div key={i} className="glass rounded-2xl p-6">
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${c.color} flex items-center justify-center mb-3`}>
              <c.icon className="w-6 h-6 text-white" />
            </div>
            <div className="text-3xl font-bold mb-1">{c.value}</div>
            <div className="text-sm text-gray-400">{c.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <a href="/startups/create" className="glass rounded-2xl p-6 hover:bg-white/10 transition">
          <Rocket className="w-8 h-8 text-purple-400 mb-3" />
          <h3 className="text-lg font-semibold mb-1">Create Startup</h3>
          <p className="text-sm text-gray-400">Yangi startap yarating va dunyoga tanishtiring</p>
        </a>
        <a href="/ai" className="glass rounded-2xl p-6 hover:bg-white/10 transition">
          <Sparkles className="w-8 h-8 text-pink-400 mb-3" />
          <h3 className="text-lg font-semibold mb-1">AI Assistant</h3>
          <p className="text-sm text-gray-400">AI bilan g'oya, biznes reja, kod yozing</p>
        </a>
        <a href="/freelancers/services/create" className="glass rounded-2xl p-6 hover:bg-white/10 transition">
          <Briefcase className="w-8 h-8 text-blue-400 mb-3" />
          <h3 className="text-lg font-semibold mb-1">Create Service</h3>
          <p className="text-sm text-gray-400">Xizmat yarating va buyurtmalar qabul qiling</p>
        </a>
        <a href="/messages" className="glass rounded-2xl p-6 hover:bg-white/10 transition">
          <MessageCircle className="w-8 h-8 text-green-400 mb-3" />
          <h3 className="text-lg font-semibold mb-1">Messages</h3>
          <p className="text-sm text-gray-400">Xabarlar va chatlar</p>
        </a>
      </div>
    </div>
  );
}
