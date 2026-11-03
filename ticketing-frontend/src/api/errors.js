export function getErrorMessage(error, fallbackMessage) {
  if (!error?.data) {
    return fallbackMessage;
  }

  if (error.data.detail) {
    return error.data.detail;
  }

  const firstError = Object.values(error.data)[0];

  if (!firstError) {
    return fallbackMessage;
  }

  if (Array.isArray(firstError)) {
    return firstError[0];
  }

  return firstError;
}