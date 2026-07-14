"use client";
import { useTranslations } from "next-intl";
import { Github, Send, Mail, Sparkles } from "lucide-react";
import Link from "next/link";

export function Footer() {
  const t = useTranslations("footer");
  return (
    <footer className="relative px-4 py-12 border-t border-white/10 mt-20">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <span className="text-lg font-bold gradient-text">00o.uz</span>
            </div>
            <p className="text-sm text-gray-400">{t("copyright")}</p>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Product</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link href="/startups" className="hover:text-purple-400">Startups</Link></li>
              <li><Link href="/freelancers" className="hover:text-purple-400">Freelancers</Link></li>
              <li><Link href="/investors" className="hover:text-purple-400">Investors</Link></li>
              <li><Link href="/ai" className="hover:text-purple-400">AI Assistant</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Company</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><a href="#" className="hover:text-purple-400">About</a></li>
              <li><a href="#" className="hover:text-purple-400">Blog</a></li>
              <li><a href="mailto:f91186645@gmail.com" className="hover:text-purple-400">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-3">Connect</h4>
            <div className="flex gap-3">
              <a href="https://github.com/KRYZENSYS" target="_blank" rel="noopener"
                 className="w-9 h-9 rounded-lg glass flex items-center justify-center hover:bg-white/10">
                <Github className="w-4 h-4" />
              </a>
              <a href="https://t.me/FirdavsVIP" target="_blank" rel="noopener"
                 className="w-9 h-9 rounded-lg glass flex items-center justify-center hover:bg-white/10">
                <Send className="w-4 h-4" />
              </a>
              <a href="mailto:f91186645@gmail.com"
                 className="w-9 h-9 rounded-lg glass flex items-center justify-center hover:bg-white/10">
                <Mail className="w-4 h-4" />
              </a>
            </div>
          </div>
        </div>
        <div className="pt-8 border-t border-white/10 flex flex-col sm:flex-row justify-between items-center gap-4">
          <p className="text-sm text-gray-400">{t("copyright")}</p>
          <p className="text-sm text-gray-400">
            Made by <a href="https://t.me/FirdavsVIP" className="text-purple-400 hover:underline">@FirdavsVIP</a> · KRYZENSYS
          </p>
        </div>
      </div>
    </footer>
  );
}
