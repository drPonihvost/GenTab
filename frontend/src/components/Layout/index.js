import React from 'react';
import cookie from 'js-cookie';
import { Avatar, Tooltip, PageHeader } from 'antd';
import { UserOutlined } from '@ant-design/icons';

import { AuthContext } from '../../Auth';
import './styles.css';

const Layout = ({ children }) => {
  const { setAuth }= React.useContext(AuthContext);

  const handleLogout = () => {
    setAuth(false);
    cookie.remove('token');
  }

  return (
    <div className="layout">
      <PageHeader
        title="Genotype"
        extra={[
          <Tooltip title="Выйти" key="avatar">
            <Avatar icon={<UserOutlined />} onClick={handleLogout} className="layout-avatar" />
          </Tooltip >
        ]}
      />
      <div className="layout-content">{children}</div>
    </div>
  )
}

export { Layout };