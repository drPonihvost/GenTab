import {
  REQUEST_URL,
  processRequest,
  getQuery,
  AUTH_HEADERS,
  COMMON_HEADERS
} from './common';

const uploadFile = (file) => {
  const formData = new FormData();
  formData.append('file', file);

  return fetch(`${REQUEST_URL}/upload`, {
    headers: { ...AUTH_HEADERS },
    method: 'POST',
    body: formData
  }).then(processRequest);
};

const decodeProject = (project) => ({
  id: project.id,
  loadAt: new Date(project.load_at).toLocaleString('ru-RU'),
  name: project.name,
  objects: project.object.map((object) => ({
    id: object.id,
    name: object.name,
    markers: object.marker.map((marker) => ({
      id: marker.id,
      name: marker.name,
      allele1: marker.allele_1,
      allele2: marker.allele_2,
      allele3: marker.allele_3,
      allele4: marker.allele_4,
      allele5: marker.allele_5,
      allele6: marker.allele_6
    }))
  }))
});

const decodeProjects = (data) => ({
  page: data.page,
  pageSize: data.page_size,
  projects: data.project.map(decodeProject),
  totalItems: data.total_items
});

export const getProjects = (params = {}) => {
  return fetch(`${REQUEST_URL}/projects/${getQuery(params)}`, {
    headers: { ...COMMON_HEADERS },
    method: 'GET'
  })
    .then(processRequest)
    .then(decodeProjects);
};

export { uploadFile };
