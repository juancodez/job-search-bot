import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "PD Jobs Europe",
  description: "Weekly product designer job search across Europe",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "'Inter', system-ui, sans-serif", background: "#0f0f0f", color: "#f0f0f0" }}>
        {children}
      </body>
    </html>
  );
}
