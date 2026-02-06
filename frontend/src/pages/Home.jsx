import React from "react";
import GlassCard from "../components/GlassCard.jsx";

export default function Home({ offers, onPlay, playMessage }) {
  return (
    <div className="space-y-4">
      <GlassCard>
        <h2 className="text-xl font-semibold">Ласкаво просимо до PRO# Hub</h2>
        <p className="text-brand-300 mt-2">
          Виконуй офери, запрошуй друзів та грай, щоб отримувати PRO#.
        </p>
        <button
          onClick={onPlay}
          className="mt-4 w-full bg-brand-500 hover:bg-brand-300 text-white py-2 rounded-xl font-semibold"
        >
          Грати (+50k PRO#)
        </button>
        {playMessage && <p className="text-sm text-brand-300 mt-2">{playMessage}</p>}
      </GlassCard>

      <div className="space-y-3">
        {offers.map((offer) => (
          <GlassCard key={offer.id}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <h3 className="text-lg font-semibold">{offer.title}</h3>
                {offer.is_limited && (
                  <span className="inline-block mt-2 text-xs uppercase bg-brand-500/30 text-brand-300 px-2 py-1 rounded-full">
                    Лімітована пропозиція
                  </span>
                )}
              </div>
              <div className="text-right">
                <p className="text-brand-300 text-sm">Нагорода</p>
                <p className="text-xl font-bold">{offer.reward_pro} PRO#</p>
              </div>
            </div>
            <a
              href={offer.link}
              target="_blank"
              rel="noreferrer"
              className="mt-4 inline-flex text-sm text-brand-300 hover:text-white"
            >
              Перейти до офера →
            </a>
          </GlassCard>
        ))}
      </div>
    </div>
  );
}
