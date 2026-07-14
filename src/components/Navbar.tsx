"use client";
import { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Rocket, Briefcase, Wrench, Sparkles, Home, Bell, User, LogOut, Search } from "lucide-react";
import AuthModal from "./AuthModal";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const NAV = [{ href: "/", icon: Home, label: "Bosh" }, { href: "/startups", icon: Rocket, label: "Startaplar" }, { href: "/jobs", icon: Briefcase, label: "Ishlar" }, { href: "/services", icon: Wrench, label: "Xizmatlar" }, { href: "/ai", icon: Sparkles, label: "AI" }];

export default function Navbar() {
  const pathname = usePathname(); const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [showAuth, setShowAuth] = useState(false);
  const [search, setSearch] = useState("");
  const [unread, setUnread] = useState(0);
  const [showMenu, setShowMenu] = useState(false);

  if (typeof window !== "undefined" && !user) {
    const u = localStorage.getItem("user"); const t = localStorage.getItem("token");
    if (u && t) {
      try { setUser(JSON.parse(u)); } catch {}
      fetch(`${API_URL}/api/v1/notifications/unread-count`, { headers: { Authorization: `Bearer ${t}` }})
        .then(r => r.ok ? r.json() : null).then(d => d && setUnread(d.count)).catch(() => {});
    }
  }

  const logout = () => { localStorage.clear(); setUser(null); router.push("/"); };

  return (
    <>
      <nav className="sticky top-0 z-40 bg-slate-900/80 backdrop-blur-xl border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-4">
          <Link href="/" className="flex items-center gap-2 flex-shrink-0">
            <div className="w-9 h-9 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center font-bold text-white">0</div>
            <span className="text-xl font-bold text-white hidden sm:block">00o.uz</span>
          </Link>
          <div className="flex-1 max-w-md relative hidden md:block">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && router.push(`/search?q=${search}`)}
              placeholder="Qidirish..." className="w-full pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:border-purple-500 focus:outline-none" />
          </div>
          <div className="hidden lg:flex items-center gap-1">
            {NAV.map(n => { const Icon = n.icon; const active = pathname === n.href; return (
              <Link key={n.href} href={n.href} className={`px-3 py-2 rounded-lg flex items-center gap-2 text-sm ${active ? "bg-white/10 text-white" : "text-gray-400 hover:text-white"}`}>
                <Icon className="w-4 h-4" /> {n.label}
              </Link>);})}
          </div>
          <div className="flex items-center gap-2 ml-auto">
            {user ? (
              <>
                <Link href="/notifications" className="p-2 hover:bg-white/10 rounded-lg relative">
                  <Bell className="w-5 h-5 text-white" />
                  {unread > 0 && <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">{unread}</span>}
                </Link>
                <div className="relative">
                  <button onClick={() => setShowMenu(!showMenu)} className="flex items-center gap-2 p-1 hover:bg-white/10 rounded-lg">
                    <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white font-bold text-sm">{user.full_name?.[0] || "U"}</div>
                    {user.is_premium && <span className="text-yellow-400 text-xs">💎</span>}
                  </button>
                  {showMenu && (
                    <div className="absolute right-0 mt-2 w-56 bg-slate-800 border border-white/10 rounded-xl shadow-2xl py-2">
                      <div className="px-4 py-2 border-b border-white/10">
                        <div className="text-white font-medium">{user.full_name}</div>
                        <div className="text-gray-400 text-sm">@{user.username}</div>
                      </div>
                      <Link href="/profile" className="px-4 py-2 hover:bg-white/5 flex items-center gap-2 text-white text-sm"><User className="w-4 h-4" />Profil</Link>
                      {user.role === "admin" && <Link href="/admin" className="px-4 py-2 hover:bg-white/5 flex items-center gap-2 text-red-400 text-sm">🛡️ Admin</Link>}
                      <button onClick={logout} className="w-full text-left px-4 py-2 hover:bg-white/5 flex items-center gap-2 text-red-400 text-sm"><LogOut className="w-4 h-4" />Chiqish</button>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <>
                <button onClick={() => setShowAuth(true)} className="px-4 py-2 text-white text-sm">Kirish</button>
                <button onClick={() => setShowAuth(true)} className="px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white text-sm rounded-lg">Ro'yxat</button>
              </>
            )}
          </div>
        </div>
        <div className="lg:hidden flex items-center justify-around border-t border-white/10 px-2 py-1">
          {NAV.map(n => { const Icon = n.icon; const active = pathname === n.href; return (
            <Link key={n.href} href={n.href} className={`p-2 flex flex-col items-center gap-0.5 ${active ? "text-purple-400" : "text-gray-400"}`}>
              <Icon className="w-5 h-5" /><span className="text-xs">{n.label}</span>
            </Link>);})}
        </div>
      </nav>
      {showAuth && <AuthModal onClose={() => setShowAuth(false)} onSuccess={(u) => setUser(u)} />}
    </>
  );
}
