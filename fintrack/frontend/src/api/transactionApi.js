import api from "./axios";

export async function createTransaction(portfolioId, payload) {
  const { data } = await api.post(`/portfolios/${portfolioId}/transactions`, payload);
  return data;
}

export async function deleteTransaction(id) {
  await api.delete(`/transactions/${id}`);
}
