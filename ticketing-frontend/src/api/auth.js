import { apiRequest } from "./client";

const ACCESS_TOKEN_KEY = "ticketfast_access_token";
const REFRESH_TOKEN_KEY = "ticketfast_refresh_token";
const USERNAME_KEY = "ticketfast_username";

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function getUsername() {
  return localStorage.getItem(USERNAME_KEY);
}

export function saveTokens({ access, refresh }) {
  localStorage.setItem(ACCESS_TOKEN_KEY, access);
  localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
}

export function saveUsername(username) {
  localStorage.setItem(USERNAME_KEY, username);
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USERNAME_KEY);
}

export function isLoggedIn() {
  return Boolean(getAccessToken());
}

export function logout() {
  clearTokens();
}

export async function fetchCurrentUser() {
  return apiRequest("/api/auth/me/");
}