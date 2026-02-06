const API_URL = import.meta.env.VITE_BACKEND_URL || window.location.origin;

export const getTelegramInitData = () => {
  if (window.Telegram && window.Telegram.WebApp) {
    return window.Telegram.WebApp.initData;
  }

  const getRawParam = (raw, key) => {
    const params = raw.replace(/^\\?/, "").replace(/^#/, "").split("&");
    for (const pair of params) {
      if (pair.startsWith(`${key}=`)) {
        return pair.substring(key.length + 1);
      }
    }
    return "";
  };

  const dataFromQuery = getRawParam(window.location.search, "tgWebAppData");
  if (dataFromQuery) {
    return dataFromQuery;
  }
  if (window.location.hash) {
    const dataFromHash = getRawParam(window.location.hash, "tgWebAppData");
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
    const error = new Error(errorText || "Помилка запиту");
    error.status = response.status;
    throw error;
  }

  return response.json();
};

export const authTelegram = async (initData) => {
  return apiRequest("/api/auth/telegram", {
    method: "POST",
    body: JSON.stringify({ initData })
  });
};
