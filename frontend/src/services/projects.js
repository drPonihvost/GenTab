import { REQUEST_URL, processRequest, AUTH_HEADERS } from './common';

const uploadFile = (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return fetch(
    `${REQUEST_URL}/upload`,
    {
      headers: { ...AUTH_HEADERS },
      method: 'POST',
      body: formData
    }
  )
    .then(processRequest);
};

export { uploadFile };