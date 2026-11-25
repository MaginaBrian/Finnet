export function validateLogin({ username, password }) {
  const errors = {};
  if (!username.trim()) errors.username = "Enter your username.";
  if (!password) errors.password = "Enter your password.";
  return errors;
}

export function validateRegister({ username, password, confirm }) {
  const errors = {};
  if (!/^[A-Za-z0-9._-]{3,50}$/.test(username.trim())) {
    errors.username = "Use 3-50 letters, numbers, dots, dashes or underscores.";
  }
  if (password.length < 8) errors.password = "Password must be at least 8 characters.";
  if (confirm !== password) errors.confirm = "Passwords do not match.";
  return errors;
}

export function validatePortfolio({ name, client_name, base_currency }) {
  const errors = {};
  if (!name.trim()) errors.name = "Enter a portfolio name.";
  if (!client_name.trim()) errors.client_name = "Enter the client's name.";
  if (!["KES", "USD"].includes(base_currency)) errors.base_currency = "Choose KES or USD.";
  return errors;
}

export function validateTransaction({ instrument, type, quantity, unit_price, trade_date }, today) {
  const errors = {};
  if (!/^[A-Za-z0-9][A-Za-z0-9.-]{0,19}$/.test(instrument.trim())) {
    errors.instrument = "Use letters, numbers, dots or dashes (e.g. SCOM, T-BILL-91).";
  }
  if (!["BUY", "SELL"].includes(type)) errors.type = "Choose BUY or SELL.";
  if (!(Number(quantity) > 0)) errors.quantity = "Quantity must be greater than zero.";
  if (!(Number(unit_price) > 0)) errors.unit_price = "Unit price must be greater than zero.";
  if (!trade_date) errors.trade_date = "Choose a trade date.";
  else if (trade_date > today) errors.trade_date = "Trade date cannot be in the future.";
  return errors;
}

export function hasErrors(errors) {
  return Object.keys(errors).length > 0;
}
