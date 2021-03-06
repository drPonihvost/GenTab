import React from 'react';

import { Upload, Typography, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

import { uploadFile } from '../../services';
import { Layout } from '../Layout';
import './styles.css';

const MainPage = () => {
  const [ files, setFiles ] = React.useState([]);
  const [ isLoading, setLoading ] = React.useState(false);

  const handleUpload = async () => {
    const [ file ] = files;

    setLoading(true);

    try {
      await uploadFile(file);
      
      setLoading(false);
      setFiles([]);
    } catch (e) {
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
    <Layout>
      <div className="main-upload">
        <Typography.Title level={4}>
          Загрузка файла проекта
        </Typography.Title>
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
          className="main-upload-button"
          onClick={handleUpload}
        >
          {isLoading ? 'Загружаем' : 'Загрузить'}
        </Button>
      </div>
    </Layout>
  );
}

export { MainPage };