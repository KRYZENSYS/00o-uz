"use client";
import { useState, useEffect } from "react";
import { ShoppingBag, Search, Heart, Star, ShoppingCart, Plus, Filter, X } from "lucide-react";
import Link from "next/link";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function MarketPage() {
  const [products, setProducts] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [cart, setCart] = useState<any>({ items: [], total: 0 });
  const [showCart, setShowCart] = useState(false);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");

  useEffect(() => { loadCategories(); loadProducts(); loadCart(); }, [category]);

  const loadCategories = async () => {
    try { const r = await fetch(`${API_URL}/api/v1/market/categories`); if (r.ok) setCategories(await r.json()); } catch {}
  };

  const loadProducts = async () => {
    const p = new URLSearchParams();
    if (search) p.append("search", search);
    if (category) p.append("category", category);
    try { const r = await fetch(`${API_URL}/api/v1/market/products?${p}`); if (r.ok) setProducts(await r.json()); } catch {}
  };

  const loadCart = async () => {
    const t = localStorage.getItem("token");
    if (!t) return;
    try { const r = await fetch(`${API_URL}/api/v1/market/cart`, { headers: { Authorization: `Bearer ${t}` } }); if (r.ok) setCart(await r.json()); } catch {}
  };

  const addToCart = async (productId: number) => {
    const t = localStorage.getItem("token");
    if (!t) return alert("Avval kiring");
    await fetch(`${API_URL}/api/v1/market/cart/add`, { method: "POST", headers: { Authorization: `Bearer ${t}`, "Content-Type": "application/json" }, body: JSON.stringify({ product_id: productId, quantity: 1 }) });
    loadCart();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-orange-900 to-slate-900 text-white p-4 md:p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold flex items-center gap-3"><ShoppingBag className="w-8 h-8 text-orange-400" /> Market</h1>
          <div className="flex items-center gap-2">
            <button onClick={() => setShowCart(true)} className="relative px-4 py-2 bg-white/10 rounded-xl flex items-center gap-2">
              <ShoppingCart className="w-4 h-4" /> Savat
              {cart.items_count > 0 && <span className="absolute -top-1 -right-1 w-5 h-5 bg-orange-500 text-xs rounded-full flex items-center justify-center">{cart.items_count}</span>}
            </button>
            <Link href="/market/sell" className="px-4 py-2 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl text-sm flex items-center gap-1"><Plus className="w-4 h-4" /> Sotish</Link>
          </div>
        </div>

        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl p-4 mb-6">
          <div className="relative mb-3">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input value={search} onChange={(e) => setSearch(e.target.value)} onKeyDown={(e) => e.key === "Enter" && loadProducts()}
              placeholder="Mahsulot qidirish..." className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:border-orange-500 focus:outline-none" />
          </div>
          <div className="flex gap-2 overflow-x-auto pb-2">
            <button onClick={() => setCategory("")} className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap ${!category ? "bg-orange-500" : "bg-white/5"}`}>Barchasi</button>
            {categories.map((c: any) => (
              <button key={c.id} onClick={() => setCategory(c.id)} className={`px-4 py-2 rounded-lg text-sm whitespace-nowrap ${category === c.id ? "bg-orange-500" : "bg-white/5"}`}>{c.name}</button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {products.map((p: any) => (
            <div key={p.id} className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl overflow-hidden hover:border-orange-500/50 transition group">
              <div className="aspect-square bg-gradient-to-br from-orange-500/20 to-red-500/20 relative">
                {p.images?.[0] ? <img src={p.images[0]} alt={p.name} className="w-full h-full object-cover" /> : <div className="flex items-center justify-center h-full text-6xl">📦</div>}
                {p.discount > 0 && <div className="absolute top-2 left-2 px-2 py-0.5 bg-red-500 text-xs rounded-full font-bold">-{p.discount}%</div>}
                <button className="absolute top-2 right-2 p-1.5 bg-black/30 backdrop-blur rounded-full"><Heart className="w-4 h-4" /></button>
              </div>
              <div className="p-3">
                <h3 className="font-semibold text-sm line-clamp-2 mb-1 min-h-[2.5rem]">{p.name}</h3>
                <div className="flex items-center gap-1 text-xs text-gray-400 mb-2">
                  <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" /> {p.rating} ({p.reviews_count})
                </div>
                <div className="flex items-end gap-2 mb-2">
                  <div className="text-lg font-bold text-orange-400">{Math.round(p.price).toLocaleString()}</div>
                  {p.old_price && <div className="text-xs text-gray-500 line-through">{Math.round(p.old_price).toLocaleString()}</div>}
                </div>
                <button onClick={() => addToCart(p.id)} className="w-full py-2 bg-gradient-to-r from-orange-500 to-red-500 rounded-lg text-sm font-medium">Savatga</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {showCart && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur flex items-end md:items-center justify-center" onClick={() => setShowCart(false)}>
          <div className="bg-slate-900 border border-white/10 rounded-t-2xl md:rounded-2xl p-6 max-w-md w-full max-h-[80vh] flex flex-col" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold flex items-center gap-2"><ShoppingCart className="w-5 h-5" /> Savat</h2>
              <button onClick={() => setShowCart(false)}><X className="w-5 h-5" /></button>
            </div>
            <div className="flex-1 overflow-y-auto space-y-2 mb-4">
              {cart.items?.length === 0 ? <p className="text-center text-gray-400 py-8">Savat bo'sh</p> :
                cart.items?.map((item: any) => (
                  <div key={item.id} className="flex items-center gap-3 p-2 bg-white/5 rounded-xl">
                    <div className="w-16 h-16 bg-gradient-to-br from-orange-500/20 to-red-500/20 rounded-lg">{item.product.images?.[0] && <img src={item.product.images[0]} className="w-full h-full object-cover rounded-lg" />}</div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium truncate">{item.product.name}</div>
                      <div className="text-xs text-gray-400">x{item.quantity}</div>
                      <div className="text-sm font-bold text-orange-400">{item.subtotal.toLocaleString()} so'm</div>
                    </div>
                  </div>
                ))}
            </div>
            {cart.items?.length > 0 && (
              <Link href="/market/checkout" className="w-full py-3 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl font-bold text-center block">
                Buyurtma berish — {cart.total.toLocaleString()} so'm
              </Link>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
