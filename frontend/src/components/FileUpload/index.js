import React from 'react';

import { Upload, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

import { uploadFile } from '../../services';

import styles from './styles.module.css';

export const FileUpload = ({ className }) => {
  const [ files, setFiles ] = React.useState([]);
  const [ isLoading, setLoading ] = React.useState(false);

  const handleUpload = async () => {
    const [ file ] = files;

    setLoading(true);

    try {
      await uploadFile(file);
      
      setLoading(false);
      setFiles([]);
    } catch(e) {
      setLoading(false);
      message.error(e.message);
    }
  };

  const handleRemove = (file) => {
    setFiles([]);
  };

  const handleBeforeUpload = (file) => {
    const isValid = file.type === 'text/plain';
    
    if (!isValid) {
      message.error(`${file.name} не является txt файлом`);

      return false;
    }

    setFiles([ file ]);

    return false;
  };


  return (
    <div className={className}>
      <Upload
          name="file"
          disabled={isLoading}
          maxCount={1}
          onRemove={handleRemove}
          beforeUpload={handleBeforeUpload}
          fileList={files}
      >
        <Button icon={<UploadOutlined />}>Выберите файл</Button>
      </Upload>
      <Button
        disabled={!files.length}
        loading={isLoading} 
        type="primary" 
        className={styles.button}
        onClick={handleUpload}
      >
        {isLoading ? 'Загружаем' : 'Загрузить'}
      </Button>
    </div>
  )
}