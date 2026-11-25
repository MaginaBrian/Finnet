import api from "./axios";

export async function listPortfolios() {
  const { data } = await api.get("/portfolios");
  return data.data;
}

export async function createPortfolio(payload) {
  const { data } = await api.post("/portfolios", payload);
  return data;
}

export async function getPortfolio(id) {
  const [portfolioRes, summaryRes, transactionRes] = await Promise.all([
    api.get(`/portfolios/${id}`),
    api.get(`/portfolios/${id}/summary`),
    api.get(`/portfolios/${id}/transactions`, { params: { per_page: 100 } }),
  ]);
  return {
    ...portfolioRes.data,
    holdings: summaryRes.data.holdings,
    totals: summaryRes.data.totals,
    transactions: transactionRes.data.data,
  };
}

export async function deletePortfolio(id) {
  await api.delete(`/portfolios/${id}`);
}

export async function fetchSummary() {
  const portfolios = await listPortfolios();
  return {
    portfolio_count: portfolios.length,
    portfolios,
    recent_transactions: [],
  };
}
