import React from 'react';
import cookie from 'js-cookie';

import { Form, Input, Button, Alert } from 'antd';

import { AuthContext } from '../../Auth';
import { getToken } from '../../services';

import styles from './styles.module.css';

const LoginPage = () => {
  const [invalid, setInvalid] = React.useState(false);
  const { setAuth } = React.useContext(AuthContext);

  const handleLogin = async ({ username, password }) => {
    try {
      const { token } = await getToken({ username, password });

      if (token) {
        setAuth(true);
        cookie.set('token', token);
      }
    } catch (e) {
      setInvalid(true);
    }
  };

  const handleInputFocus = () => {
    setInvalid(false);
  };

  return (
    <div className={styles.login}>
      {invalid && (
        <Alert message="Неверный логин или пароль" type="error" showIcon />
      )}
      <Form name="login" layout="vertical" size="large" onFinish={handleLogin}>
        <Form.Item
          label="Имя"
          name="username"
          rules={[
            {
              required: true,
              message: 'Обязательное поле'
            }
          ]}
        >
          <Input onFocus={handleInputFocus} />
        </Form.Item>

        <Form.Item
          label="Пароль"
          name="password"
          rules={[
            {
              required: true,
              message: 'Обязательное поле'
            }
          ]}
        >
          <Input.Password onFocus={handleInputFocus} />
        </Form.Item>

        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            className={styles.submit}
            block
          >
            Войти
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export { LoginPage };
