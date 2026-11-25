const BASE_URL = (import.meta.env.VITE_API_URL || "http://localhost:5000").replace(/\/+$/, "");

let getToken = () => null;
let onUnauthorized = () => {};

export function configureClient(options) {
  getToken = options.getToken ?? getToken;
  onUnauthorized = options.onUnauthorized ?? onUnauthorized;
}

export class ApiError extends Error {
  constructor(status, code, message, details = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

function buildUrl(path, query) {
  const params = new URLSearchParams(
    Object.entries(query ?? {}).filter(([, v]) => v !== "" && v !== null && v !== undefined),
  ).toString();
  return `${BASE_URL}${path}${params ? `?${params}` : ""}`;
}

export async function request(path, { method = "GET", body, query, signal, auth = true, blob = false } = {}) {
  const headers = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  const token = getToken();
  if (auth && token) headers.Authorization = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(buildUrl(path, query), {
      method,
      headers,
      signal,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch (err) {
    if (err.name === "AbortError") throw err;
    throw new ApiError(0, "network_error", "Can't reach the server. Check your connection and try again.");
  }

  if (!response.ok) {
    let payload = null;
    try {
      payload = await response.json();
    } catch {

    }
    const err = payload?.error;
    if (response.status === 401 && auth) onUnauthorized();
    throw new ApiError(
      response.status,
      err?.code ?? "http_error",
      err?.message ?? `Request failed (${response.status}).`,
      err?.details ?? {},
    );
  }

  if (response.status === 204) return null;
  return blob ? response.blob() : response.json();
}
