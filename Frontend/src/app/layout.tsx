import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import HomeButton from "./components/HomeButton"
import { I18nProvider } from "./components/I18nProvider"
import { LanguageSwitcher } from "./components/LanguageSwitcher"


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Exia",
  description: "Explore planets and play the exoplanet classification game",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <I18nProvider>
          <HomeButton />
          <LanguageSwitcher />
          {children}
        </I18nProvider>
      </body>
    </html>
  );
}
