import { request } from "./client";

export const listTransactions = (portfolioId, query, signal) =>
  request(`/api/portfolios/${portfolioId}/transactions`, { query, signal });

export const createTransaction = (portfolioId, body) =>
  request(`/api/portfolios/${portfolioId}/transactions`, { method: "POST", body });

export const deleteTransaction = (id) => request(`/api/transactions/${id}`, { method: "DELETE" });

export const exportTransactionsCsv = (portfolioId, query) =>
  request(`/api/portfolios/${portfolioId}/transactions/export.csv`, { query, blob: true });
