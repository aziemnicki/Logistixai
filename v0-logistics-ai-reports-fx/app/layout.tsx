import type { Metadata } from "next"
import type React from "react"

import { Analytics } from "@vercel/analytics/next"
import "./globals.css"
import { Inter } from "next/font/google"
import { Geist_Mono } from "next/font/google"
import { APIKeyProvider } from "@/lib/api-key-context"

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-inter",
})

const geistMono = Geist_Mono({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-mono",
})

export const metadata: Metadata = {
  title: "Cyberlogix.ai - Predict, Prevent, Comply, and Stay ahead of any shift in logistics.",
  description:
    "AI-powered intelligence platform for logistics companies providing regulatory compliance, operational insights, and strategic forecasting.",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${geistMono.variable} font-sans antialiased`}>
        <APIKeyProvider>
          {children}
          <Analytics />
        </APIKeyProvider>
      </body>
    </html>
  )
}
