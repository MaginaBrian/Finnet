import api from "./axios";

export async function createTransaction(portfolioId, payload) {
  const { data } = await api.post(`/portfolios/${portfolioId}/transactions`, payload);
  return data.data;
}

export async function deleteTransaction(id) {
  const { data } = await api.delete(`/transactions/${id}`);
  return data.data;
}
