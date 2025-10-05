import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || '/api',
  },
  eslint: {
    // Disable ESLint during builds in Docker
    ignoreDuringBuilds: process.env.NODE_ENV === 'production' && process.env.DOCKER_BUILD === 'true',
  },
  typescript: {
    // Disable TypeScript errors during builds in Docker
    ignoreBuildErrors: process.env.NODE_ENV === 'production' && process.env.DOCKER_BUILD === 'true',
  },
  // Remove rewrites for Vercel deployment - API routes will be handled by Vercel
  output: 'standalone',
};

export default nextConfig;