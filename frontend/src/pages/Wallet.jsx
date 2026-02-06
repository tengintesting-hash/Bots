import React from "react";
import GlassCard from "../components/GlassCard.jsx";

export default function Wallet({ wallet, onWithdraw, withdrawMessage }) {
  return (
    <div className="space-y-4">
      <GlassCard>
        <h2 className="text-xl font-semibold">Ваш баланс</h2>
        <div className="mt-4 space-y-2">
          <div className="flex justify-between">
            <span className="text-brand-300">PRO#</span>
            <span className="text-xl font-bold">{wallet.balance_pro}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-brand-300">USD</span>
            <span className="text-xl font-bold">${wallet.balance_usd}</span>
          </div>
        </div>
      </GlassCard>

      <GlassCard>
        <h3 className="text-lg font-semibold">Виведення коштів</h3>
        <button
          onClick={onWithdraw}
          className="mt-3 w-full bg-brand-500 hover:bg-brand-300 text-white py-2 rounded-xl font-semibold"
        >
          Вивести кошти
        </button>
        {withdrawMessage && <p className="text-sm text-brand-300 mt-2">{withdrawMessage}</p>}
      </GlassCard>
    </div>
  );
}
