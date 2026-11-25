import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export function messageFrom(err) {
  const error = err.response?.data?.error;
  if (!error) return "";
  if (typeof error === "string") return error;
  return error.message || "";
}

export default api;
