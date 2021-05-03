import React from 'react';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';

import { AuthContext } from './Auth';
import { LoginPage } from './components/LoginPage';
import { MainPage } from './components/MainPage';

const ProtectedRoute = ({ component: Component, auth, ...props }) => (
  <Route
    {...props}
    render={
      () => auth ? (
        <Component />
      ) : (
        <Redirect to='/login' />
      )
    }
  />
);

const ProtectedLogin = ({ component: Component, auth, ...props }) => (
  <Route
    {...props}
    render={
      () => auth ? (
        <Redirect to='/' />
      ) : (
        <Component />
      )
    }
  />
);


const Routes = () => {
  const { auth } = React.useContext(AuthContext);

  return (
    <BrowserRouter>
      <Switch>
        <ProtectedLogin path='/login' component={LoginPage} auth={auth} />
        <ProtectedRoute path='/' component={MainPage} auth={auth} />
      </Switch>
    </BrowserRouter>
  );
}

export { Routes };