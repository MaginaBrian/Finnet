import { request } from "./client";

export const login = (username, password) =>
  request("/api/auth/login", { method: "POST", body: { username, password }, auth: false });

export const register = (username, password, full_name) =>
  request("/api/auth/register", { method: "POST", body: { username, password, full_name }, auth: false });

export const fetchMe = (signal) => request("/api/auth/me", { signal });
