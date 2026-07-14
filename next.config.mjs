import createNextIntlPlugin from 'next-intl/plugin';

const withNextIntl = createNextIntlPlugin('./src/i18n/request.ts');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'res.cloudinary.com' },
      { protocol: 'https', hostname: 'avatars.githubusercontent.com' },
      { protocol: 'https', hostname: 'lh3.googleusercontent.com' },
      { protocol: 'https', hostname: 't.me' },
    ],
  },
  experimental: {
    optimizePackageImports: ['lucide-react', '@radix-ui/react-icons'],
  },
  async rewrites() {
    return [
      { source: '/api/v1/:path*', destination: `${process.env.NEXT_PUBLIC_API_URL}/api/v1/:path*` },
      { source: '/ws/:path*', destination: `${process.env.NEXT_PUBLIC_WS_URL}/ws/:path*` },
    ];
  },
};

export default withNextIntl(nextConfig);
