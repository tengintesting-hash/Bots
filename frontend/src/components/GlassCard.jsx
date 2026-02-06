import React from "react";

export default function GlassCard({ children }) {
  return (
    <div className="bg-brand-800/80 border border-brand-700/60 rounded-2xl p-4 shadow-xl">
      {children}
    </div>
  );
}
