import { request } from "./client";

export const listPortfolios = (signal) => request("/api/portfolios", { signal });
export const getPortfolio = (id, signal) => request(`/api/portfolios/${id}`, { signal });
export const createPortfolio = (body) => request("/api/portfolios", { method: "POST", body });
export const updatePortfolio = (id, body) => request(`/api/portfolios/${id}`, { method: "PUT", body });
export const deletePortfolio = (id) => request(`/api/portfolios/${id}`, { method: "DELETE" });
export const getSummary = (id, signal) => request(`/api/portfolios/${id}/summary`, { signal });
