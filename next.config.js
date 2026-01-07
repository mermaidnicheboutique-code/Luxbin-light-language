/** @type {import('next').NextConfig} */
const nextConfig = {
  // Removed 'output: export' to enable API routes
  images: { unoptimized: true },
  // Force fresh Vercel deployment
}

module.exports = nextConfig