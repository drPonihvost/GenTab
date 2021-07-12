import React from 'react';

import { Modal, Button } from 'antd';
import { MinusOutlined } from '@ant-design/icons';

import styles from './styles.module.css';

export const MergeModal = ({
  visible,
  items,
  onFlush,
  onAdd,
  onCancel,
  onDelete
}) => (
  <Modal
    title="Объекты для объединения"
    visible={visible}
    onCancel={onCancel}
    centered
    footer={[
      <Button key="flush" danger onClick={onFlush}>
        Очистить всё
      </Button>,
      <Button key="add" type="primary" onClick={onAdd}>
        Добавить в таблицу
      </Button>
    ]}
  >
    {Object.keys(items).map((objectName) => (
      <div key={objectName} className={styles.object}>
        <div className={styles.delete}>{items[objectName].name}</div>
        <Button
          key="flash"
          type="secondary"
          size="small"
          danger
          onClick={() => onDelete(objectName)}
        >
          <MinusOutlined />
        </Button>
      </div>
    ))}
  </Modal>
);
