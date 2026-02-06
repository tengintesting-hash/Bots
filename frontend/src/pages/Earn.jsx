import React from "react";
import GlassCard from "../components/GlassCard.jsx";

export default function Earn({ stats, referralLink, onCopy }) {
  return (
    <div className="space-y-4">
      <GlassCard>
        <h2 className="text-xl font-semibold">Реферальна програма</h2>
        <p className="text-brand-300 mt-2">
          Запрошуй друзів та отримуй винагороду за їхні депозити.
        </p>
        <div className="mt-4 space-y-2">
          <div className="flex justify-between">
            <span className="text-brand-300">Усього рефералів</span>
            <span className="font-semibold">{stats.total_referrals}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-brand-300">Рефералів з депозитом</span>
            <span className="font-semibold">{stats.deposit_referrals}</span>
          </div>
        </div>
      </GlassCard>

      <GlassCard>
        <h3 className="text-lg font-semibold">Ваше посилання</h3>
        <p className="text-brand-300 text-sm break-all mt-2">{referralLink}</p>
        <button
          onClick={onCopy}
          className="mt-3 w-full bg-brand-500 hover:bg-brand-300 text-white py-2 rounded-xl font-semibold"
        >
          Копіювати посилання
        </button>
      </GlassCard>
    </div>
  );
}
