import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  eslint: {
    // Disable ESLint during builds in Docker
    ignoreDuringBuilds: process.env.NODE_ENV === 'production' && process.env.DOCKER_BUILD === 'true',
  },
  typescript: {
    // Disable TypeScript errors during builds in Docker
    ignoreBuildErrors: process.env.NODE_ENV === 'production' && process.env.DOCKER_BUILD === 'true',
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/:path*`,
      },
    ];
  },
};

export default nextConfig;