"use client";
import { useEffect, useState } from "react";
import { Rocket, Filter, Plus, TrendingUp, Heart, Users, ExternalLink } from "lucide-react";
import Link from "next/link";

const categories = ["All", "Fintech", "EdTech", "HealthTech", "AgriTech", "AI", "Ecommerce", "SaaS"];

const mockStartups = [
  { id: 1, name: "PayUz", tagline: "Mobile payment platform", category: "Fintech", logo: "💳", stage: "Growth", funding_goal: 500000, funding_raised: 250000, team_size: 8, location: "Tashkent" },
  { id: 2, name: "EduMaster", tagline: "Online learning for schools", category: "EdTech", logo: "📚", stage: "MVP", funding_goal: 200000, funding_raised: 120000, team_size: 5, location: "Samarkand" },
  { id: 3, name: "AgroSmart", tagline: "Smart farming solutions", category: "AgriTech", logo: "🌾", stage: "Early", funding_goal: 300000, funding_raised: 80000, team_size: 6, location: "Bukhara" },
  { id: 4, name: "HealthPlus", tagline: "Telemedicine platform", category: "HealthTech", logo: "🏥", stage: "Growth", funding_goal: 400000, funding_raised: 200000, team_size: 12, location: "Tashkent" },
  { id: 5, name: "LogiTrack", tagline: "Logistics management", category: "SaaS", logo: "🚚", stage: "MVP", funding_goal: 250000, funding_raised: 150000, team_size: 4, location: "Tashkent" },
  { id: 6, name: "AIWriter", tagline: "AI content generator", category: "AI", logo: "🤖", stage: "Scale", funding_goal: 1000000, funding_raised: 300000, team_size: 15, location: "Remote" },
];

export default function StartupsPage() {
  const [filter, setFilter] = useState("All");
  const [startups, setStartups] = useState(mockStartups);

  const filtered = filter === "All" ? startups : startups.filter((s) => s.category === filter);

  return (
    <div className="min-h-screen max-w-7xl mx-auto px-4 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-4xl font-bold gradient-text mb-2">Startups</h1>
          <p className="text-gray-400">O'zbekistondagi barcha startaplar</p>
        </div>
        <Link href="/startups/create"
          className="px-5 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-500 font-medium flex items-center gap-2 hover:opacity-90">
          <Plus className="w-4 h-4" /> Create Startup
        </Link>
      </div>

      <div className="flex flex-wrap gap-2 mb-6">
        {categories.map((cat) => (
          <button key={cat} onClick={() => setFilter(cat)}
            className={`px-4 py-2 rounded-xl text-sm transition ${
              filter === cat ? "bg-gradient-to-r from-purple-500 to-pink-500" : "glass hover:bg-white/10"
            }`}>
            {cat}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((s) => (
          <div key={s.id} className="glass rounded-2xl p-6 hover:bg-white/10 transition">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-purple-500/30 to-pink-500/30 flex items-center justify-center text-3xl">
                  {s.logo}
                </div>
                <div>
                  <h3 className="font-semibold text-lg">{s.name}</h3>
                  <p className="text-xs text-gray-400">{s.category} · {s.stage}</p>
                </div>
              </div>
            </div>
            <p className="text-sm text-gray-300 mb-4">{s.tagline}</p>

            <div className="mb-4">
              <div className="flex justify-between text-xs text-gray-400 mb-1">
                <span>${s.funding_raised.toLocaleString()}</span>
                <span>${s.funding_goal.toLocaleString()}</span>
              </div>
              <div className="w-full h-2 rounded-full bg-white/10 overflow-hidden">
                <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500"
                  style={{ width: `${(s.funding_raised / s.funding_goal) * 100}%` }} />
              </div>
            </div>

            <div className="flex items-center justify-between text-sm text-gray-400">
              <div className="flex gap-3">
                <span className="flex items-center gap-1"><Users className="w-3 h-3" /> {s.team_size}</span>
                <span className="flex items-center gap-1">📍 {s.location}</span>
              </div>
              <a href={`/startups/${s.id}`} className="text-purple-400 hover:text-purple-300">
                <ExternalLink className="w-4 h-4" />
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
