import cookie from 'js-cookie';

export const REQUEST_URL = 'http://127.0.0.1:5000';

export const AUTH_HEADERS = {
  Authorization: `Bearer ${cookie.get('token')}`
};

export const COMMON_HEADERS = {
  ...AUTH_HEADERS,
  'Content-Type': 'application/json',
};

const processRequest = (response, opts = {}) => {
  const { withAuthRedirect = true } = opts;

  if (response.ok) {
    return response.json();
  }

  if (withAuthRedirect && response.status === 401) {
    cookie.remove('token');
    window.location.href = '/login';

    return;
  }

  throw new Error(response.statusText);
};

export { processRequest };