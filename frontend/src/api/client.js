const API_URL = import.meta.env.VITE_BACKEND_URL || window.location.origin;

export const getTelegramInitData = () => {
  if (window.Telegram && window.Telegram.WebApp) {
    return window.Telegram.WebApp.initData;
  }
  const searchParams = new URLSearchParams(window.location.search);
  const dataFromQuery = searchParams.get("tgWebAppData");
  if (dataFromQuery) {
    return dataFromQuery;
  }
  if (window.location.hash) {
    const hashParams = new URLSearchParams(window.location.hash.replace("#", ""));
    const dataFromHash = hashParams.get("tgWebAppData");
    if (dataFromHash) {
      return dataFromHash;
    }
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
