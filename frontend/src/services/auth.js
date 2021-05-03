import { REQUEST_URL, COMMON_HEADERS, processRequest } from './common';

const getToken = ({ username, password }) => fetch(
  `${REQUEST_URL}/token`,
  {
      method: 'POST',
      headers: { ...COMMON_HEADERS },
      body: JSON.stringify({
        username,
        password
      })
  }
)
  .then(res => processRequest(res, { withAuthRedirect: false }));

export { getToken };

