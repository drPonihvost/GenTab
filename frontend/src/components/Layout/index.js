import React from 'react';
import cookie from 'js-cookie';
import { Avatar, Tooltip, PageHeader } from 'antd';
import { UserOutlined } from '@ant-design/icons';

import { AuthContext } from '../../Auth';
import styles from './styles.module.css';

const Layout = ({ children, className }) => {
  const { setAuth } = React.useContext(AuthContext);

  const handleLogout = () => {
    setAuth(false);
    cookie.remove('token');
  };

  return (
    <div className={`${styles.layout} ${className}`}>
      <PageHeader
        title="Genotype"
        extra={[
          <Tooltip title="Выйти" key="avatar">
            <Avatar
              icon={<UserOutlined />}
              onClick={handleLogout}
              className={styles.avatar}
            />
          </Tooltip>
        ]}
      />
      <div className={styles.content}>{children}</div>
    </div>
  );
};

export { Layout };
