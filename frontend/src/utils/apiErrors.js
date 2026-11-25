export function splitApiError(err) {
  const details = err?.details && typeof err.details === "object" ? err.details : {};
  const hasFieldErrors = Object.keys(details).length > 0;
  return {
    fieldErrors: details,
    formError: hasFieldErrors && err.code === "validation_error" ? "" : err?.message ?? "Something went wrong.",
  };
}
