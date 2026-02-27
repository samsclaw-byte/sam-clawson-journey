/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: [],
  },
  // Alias for react-native-web compatibility
  transpilePackages: ['react-native-web'],
}

module.exports = nextConfig
