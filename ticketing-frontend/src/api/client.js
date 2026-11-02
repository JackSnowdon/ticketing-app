import {
  getAccessToken,
  getRefreshToken,
  saveTokens,
  clearTokens,
} from "./auth";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function refreshAccessToken() {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    throw new Error("No refresh token available.");
  }

  const response = await fetch(
    `${API_BASE_URL}/api/auth/token/refresh/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        refresh: refreshToken,
      }),
    }
  );

  if (!response.ok) {
    clearTokens();
    throw new Error("Unable to refresh authentication token.");
  }

  const data = await response.json();

  saveTokens({
    access: data.access,
    refresh: refreshToken,
  });

  return data.access;
}

export async function apiRequest(path, options = {}) {
  let token = getAccessToken();

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  let response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401 && getRefreshToken()) {
    try {
      token = await refreshAccessToken();

      response = await fetch(`${API_BASE_URL}${path}`, {
        ...options,
        headers: {
          ...headers,
          Authorization: `Bearer ${token}`,
        },
      });
    } catch (refreshError) {
      clearTokens();
    }
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw {
      status: response.status,
      data,
    };
  }

  return data;
}