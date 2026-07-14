/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: { unoptimized: true },
  async redirects() {
    return [
      { source: '/', destination: '/uz', permanent: false },
      { source: '/en', destination: '/en/home', permanent: false },
      { source: '/ru', destination: '/ru/home', permanent: false },
    ];
  },
  async rewrites() {
    return [
      { source: '/uz', destination: '/uz/home' },
      { source: '/ru', destination: '/ru/home' },
    ];
  },
};
module.exports = nextConfig;
