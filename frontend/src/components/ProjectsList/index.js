import React from 'react';
import {
  Spin,
  Collapse,
  Empty,
  Button,
  Pagination,
  Input,
  message
} from 'antd';
import debounce from 'lodash/debounce';

import { getProjects } from '../../services';

import styles from './styles.module.css';

export const ProjectsList = ({ className, onAddClick, onMergeClick }) => {
  const [projectsData, setProjectsData] = React.useState({});
  const [isLoading, setLoading] = React.useState(false);
  const [hoveredObjectId, setHoveredObjectId] = React.useState(null);
  const [name, setName] = React.useState('');
  const isInitialMount = React.useRef(true);

  const { page, pageSize, totalItems, projects = [] } = projectsData;

  const loadProjects = async (params = {}) => {
    setLoading(true);

    try {
      const data = await getProjects(params);
      setLoading(false);
      setProjectsData(data);
    } catch (e) {
      setLoading(false);
      message.error(e.message);
    }
  };

  const debouncedLoadProjects = React.useCallback(
    debounce(loadProjects, 500),
    []
  );

  React.useEffect(() => {
    loadProjects();
  }, []);

  React.useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;
    } else {
      debouncedLoadProjects({ name });
    }
  }, [name, debouncedLoadProjects]);

  const handlePageChange = (page) => {
    loadProjects({ page });
  };

  const handleMouseEnter = (objectId) => {
    setHoveredObjectId(objectId);
  };

  const handleMouseLeave = () => {
    setHoveredObjectId(null);
  };

  const handleNameFilterChange = (e) => {
    const value = e.target.value;

    setName(value);
  };

  let content = <Empty description="У вас нет загруженных проектов" />;

  if (isLoading) {
    content = (
      <div className={styles.spinner}>
        <Spin delay={300} size="large" />
      </div>
    );
  }

  if (!isLoading && projects.length) {
    content = projects.map((project) => (
      <Collapse className={styles.row} key={project.id}>
        <Collapse.Panel header={project.name} extra={project.loadAt}>
          {project.objects.map((object) => (
            <div
              onMouseEnter={() => handleMouseEnter(object.id)}
              onMouseLeave={handleMouseLeave}
              className={styles.object}
              key={object.id}
            >
              {object.name}
              {hoveredObjectId === object.id && (
                <div className={styles.controls}>
                  <Button
                    type="primary"
                    size="small"
                    onClick={() => onAddClick(object)}
                    className={styles.addButton}
                  >
                    Добавить
                  </Button>
                  <Button size="small" onClick={() => onMergeClick(object)}>
                    Добавить для объединения
                  </Button>
                </div>
              )}
            </div>
          ))}
        </Collapse.Panel>
      </Collapse>
    ));
  }

  return (
    <div className={className}>
      <Input
        value={name}
        onChange={handleNameFilterChange}
        placeholder="Введите имя проекта"
        size="large"
        className={styles.filterInput}
      />
      {content}
      {totalItems > pageSize && (
        <Pagination
          defaultCurrent={1}
          current={page}
          pageSize={pageSize}
          total={totalItems}
          onChange={handlePageChange}
          className={styles.pager}
        />
      )}
    </div>
  );
};
