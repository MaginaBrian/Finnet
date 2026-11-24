import api from "./axios";

export async function listPortfolios() {
  const { data } = await api.get("/portfolios");
  return data.data;
}

export async function createPortfolio(payload) {
  const { data } = await api.post("/portfolios", payload);
  return data.data;
}

export async function getPortfolio(id) {
  const { data } = await api.get(`/portfolios/${id}`);
  return data.data;
}

export async function deletePortfolio(id) {
  const { data } = await api.delete(`/portfolios/${id}`);
  return data.data;
}

export async function fetchSummary() {
  const { data } = await api.get("/summary");
  return data.data;
}
