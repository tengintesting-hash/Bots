import React, { useEffect, useState } from "react";
import BottomTabs from "./components/BottomTabs.jsx";
import Home from "./pages/Home.jsx";
import Earn from "./pages/Earn.jsx";
import Wallet from "./pages/Wallet.jsx";
import { apiRequest, authTelegram, getTelegramInitData } from "./api/client.js";

const emptyStats = {
  total_referrals: 0,
  deposit_referrals: 0,
  reward_per_invite: 1000,
  reward_per_deposit: 5000
};

export default function App() {
  const botUsername = import.meta.env.VITE_BOT_USERNAME || "your_bot_username";
  const [activeTab, setActiveTab] = useState("home");
  const [user, setUser] = useState(null);
  const [offers, setOffers] = useState([]);
  const [stats, setStats] = useState(emptyStats);
  const [wallet, setWallet] = useState({ balance_pro: 0, balance_usd: 0 });
  const [playMessage, setPlayMessage] = useState("");
  const [withdrawMessage, setWithdrawMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const userHeader = user ? { "X-User-Id": String(user.telegram_id) } : {};

  useEffect(() => {
    const init = async () => {
      try {
        const initData = getTelegramInitData();
        if (!initData) {
          setError("Відкрийте застосунок через Telegram WebApp.");
          setLoading(false);
          return;
        }

        if (window.Telegram && window.Telegram.WebApp) {
          window.Telegram.WebApp.ready();
        }

        const authUser = await authTelegram(initData);
        setUser(authUser);
        setLoading(false);
      } catch (err) {
        setError("Не вдалося авторизуватися. Спробуйте пізніше.");
        setLoading(false);
      }
    };

    init();
  }, []);

  useEffect(() => {
    if (!user) {
      return;
    }

    const fetchData = async () => {
      const [offersData, statsData, walletData] = await Promise.all([
        apiRequest("/api/offers", { headers: userHeader }),
        apiRequest("/api/referrals", { headers: userHeader }),
        apiRequest("/api/wallet", { headers: userHeader })
      ]);
      setOffers(offersData);
      setStats(statsData);
      setWallet(walletData);
    };

    fetchData().catch(() => {
      setError("Не вдалося завантажити дані.");
    });
  }, [user]);

  const handlePlay = async () => {
    if (!user) return;
    setPlayMessage("");
    try {
      const response = await apiRequest("/api/game/play", {
        method: "POST",
        headers: userHeader
      });
      setPlayMessage(response.message);
      if (response.balance_pro) {
        setWallet((prev) => ({ ...prev, balance_pro: response.balance_pro }));
      }
    } catch (err) {
      setPlayMessage("Не вдалося активувати бонус.");
    }
  };

  const handleWithdraw = async () => {
    if (!user) return;
    setWithdrawMessage("");
    try {
      const response = await apiRequest("/api/withdraw", {
        method: "POST",
        headers: userHeader,
        body: JSON.stringify({ amount: 10000, wallet: "USDT" })
      });
      setWithdrawMessage(response.message);
    } catch (err) {
      setWithdrawMessage("Не вдалося створити заявку.");
    }
  };

  const handleCopy = async () => {
    if (!user) return;
    const link = `https://t.me/${botUsername}?start=ref_${user.telegram_id}`;
    try {
      await navigator.clipboard.writeText(link);
      setWithdrawMessage("");
    } catch (err) {
      setWithdrawMessage("Не вдалося скопіювати посилання.");
    }
  };

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Завантаження...</div>;
  }

  if (error) {
    return <div className="min-h-screen flex items-center justify-center text-center px-4">{error}</div>;
  }

  return (
    <div className="min-h-screen bg-brand-900 text-white pb-24">
      <div className="max-w-md mx-auto px-4 py-6 space-y-6">
        {activeTab === "home" && (
          <Home offers={offers} onPlay={handlePlay} playMessage={playMessage} />
        )}
        {activeTab === "earn" && (
          <Earn
            stats={stats}
            referralLink={`https://t.me/${botUsername}?start=ref_${user.telegram_id}`}
            onCopy={handleCopy}
          />
        )}
        {activeTab === "wallet" && (
          <Wallet
            wallet={wallet}
            onWithdraw={handleWithdraw}
            withdrawMessage={withdrawMessage}
          />
        )}
      </div>
      <BottomTabs active={activeTab} onChange={setActiveTab} />
    </div>
  );
}
