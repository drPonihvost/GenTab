import React from 'react';

import { Button } from 'antd';

import styles from './styles.module.css';

export const BottomPanel = ({
  className,
  selectedObjectsCount,
  objectsToMergeCount,
  onMergeObjectsShow,
  onSelectedShow
}) => {
  const selectedObjectsButtonTitle = selectedObjectsCount ?
    `Показать результат (${selectedObjectsCount})` :
    `Показать результат`;

  const objectsToMergeButtonTitle = objectsToMergeCount ?
    `Показать объединения (${objectsToMergeCount})` :
    `Показать объединения`;

  return (
    <div className={`${styles.container} ${className}`}>
      <Button type="primary" onClick={onSelectedShow} className={styles.showTableButton} disabled={!selectedObjectsCount}>
        {selectedObjectsButtonTitle}
      </Button>
      <Button type="secondary" onClick={onMergeObjectsShow} disabled={!objectsToMergeCount}>
        {objectsToMergeButtonTitle}
      </Button>
    </div>
  )
}