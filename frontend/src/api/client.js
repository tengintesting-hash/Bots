const API_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export const getTelegramInitData = () => {
  if (window.Telegram && window.Telegram.WebApp) {
    return window.Telegram.WebApp.initData;
  }
  return "";
};

export const apiRequest = async (path, options = {}) => {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {})
  };

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Помилка запиту");
  }

  return response.json();
};

export const authTelegram = async (initData) => {
  return apiRequest("/api/auth/telegram", {
    method: "POST",
    body: JSON.stringify({ initData })
  });
};
