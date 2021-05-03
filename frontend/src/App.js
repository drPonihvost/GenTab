import React from 'react';
import cookie from 'js-cookie';

import { Routes } from './Routes';
import { AuthContext } from './Auth';

import 'antd/dist/antd.css';

const App = () => {
  const [ auth, setAuth ] = React.useState(false);

  React.useEffect(() => {
    if (cookie.get('token')) {
      setAuth(true);
    };
  }, []);

  return (
    <AuthContext.Provider value={{ auth, setAuth }}>
      <Routes />
    </AuthContext.Provider>
  );
};

export { App };
