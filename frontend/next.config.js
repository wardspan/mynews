/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    env: {
      NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
    },
    images: {
      domains: ['www.example.com', 'i.guim.co.uk', 'static.guim.co.uk', 'media.guim.co.uk', 'cdn.pixabay.com', 'gnews.io'],
      remotePatterns: [
        {
          protocol: 'https',
          hostname: '**',
        },
      ],
    },
  }
  
  module.exports = nextConfig;