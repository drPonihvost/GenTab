import React from 'react';

import { Typography } from 'antd';

import { Layout } from '../Layout';
import { ProjectsList } from '../ProjectsList';
import { FileUpload } from '../FileUpload';
import { BottomPanel } from '../BottomPanel';

import styles from './styles.module.css';

const MainPage = () => {
  const [selectedObjects, setSelectedObject] = React.useState({});
  const [objectsToMerge, setObjectToMerge] = React.useState({});

  const handleAddClick = (object) => {
    setSelectedObject({ ...selectedObjects, [object.id]: object });
  };

  const handleMergeClick = (object) => {
    setObjectToMerge({ ...objectsToMerge, [object.id]: object });
  };

  const handleSelectedObjectsShow = () => {
    console.log('Когда-нить тут будет таблица');
  };

  const handleObjectsToMergeShow = () => {
    console.log('Когда-нить тут будет таблица для мержа');
  };

  const selectedObjectsCount = Object.keys(selectedObjects).length;
  const objectsToMergeCount = Object.keys(objectsToMerge).length;

  const showBottomPanel = Boolean(selectedObjectsCount || objectsToMergeCount);

  return (
    <Layout className={styles.layout}>
      <div className={styles.fileUploadContainer}>
        <Typography.Title level={4}>Загрузка файла проекта</Typography.Title>
        <FileUpload className={styles.fileUpload} />
      </div>
      <div className={styles.projectsContainer}>
        <Typography.Title level={4}>Загруженные проекты</Typography.Title>
        <ProjectsList
          className={styles.projects}
          onAddClick={handleAddClick}
          onMergeClick={handleMergeClick}
        />
        {showBottomPanel && (
          <BottomPanel
            className={styles.bottomPanel}
            selectedObjectsCount={selectedObjectsCount}
            objectsToMergeCount={objectsToMergeCount}
            onSelectedShow={handleSelectedObjectsShow}
            onMergeObjectsShow={handleObjectsToMergeShow}
          />
        )}
      </div>
    </Layout>
  );
};

export { MainPage };
