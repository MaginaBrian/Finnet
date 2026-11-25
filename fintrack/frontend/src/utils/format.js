const MINUS = "\u2212"; // true minus sign, so screen readers and sighted users agree

const number = new Intl.NumberFormat("en-KE", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});
const quantity = new Intl.NumberFormat("en-KE", { maximumFractionDigits: 4 });

/** KES 1,250,000.00 */
export function formatMoney(value, currency) {
  return `${currency} ${number.format(Math.abs(value) < 0.005 ? 0 : value)}`;
}

/** +KES 1,000.00 / −KES 1,000.00 / KES 0.00 */
export function formatSignedMoney(value, currency) {
  if (Math.abs(value) < 0.005) return formatMoney(0, currency);
  const sign = value > 0 ? "+" : MINUS;
  return `${sign}${currency} ${number.format(Math.abs(value))}`;
}

export function formatSignedPercent(value) {
  if (Math.abs(value) < 0.005) return "0.00%";
  return `${value > 0 ? "+" : MINUS}${Math.abs(value).toFixed(2)}%`;
}

export function formatPercent(value) {
  return `${value.toFixed(1)}%`;
}

export function formatQuantity(value) {
  return quantity.format(value);
}

export function formatPrice(value) {
  return number.format(value);
}

export function formatDate(iso) {
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  });
}

export function plClass(value) {
  if (Math.abs(value) < 0.005) return "";
  return value > 0 ? "pl--pos" : "pl--neg";
}

export function todayIso() {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}
