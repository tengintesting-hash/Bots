import React from "react";

const tabs = [
  { id: "home", label: "Головна" },
  { id: "earn", label: "Заробіток" },
  { id: "wallet", label: "Гаманець" }
];

export default function BottomTabs({ active, onChange }) {
  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 bg-brand-800/90 border border-brand-700/80 rounded-full px-4 py-2 flex gap-4">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          className={`text-sm font-semibold px-3 py-1 rounded-full transition ${
            active === tab.id ? "bg-brand-500 text-white" : "text-brand-300"
          }`}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}
