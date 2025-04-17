import { useState } from "react";
import { useNavigate } from "react-router-dom";
import qs from "qs";
import { Button, Input, Form, message, Typography } from "antd";
import api from "../api";
import { saveToken } from "../auth"; // если ты сохраняешь токен

const { Title } = Typography;

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await api.post(
        "/auth/login",
        qs.stringify({ username, password }), // сериализация формы
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      saveToken(response.data.access_token);
      message.success("Вы успешно вошли!");
      navigate("/projects");
    } catch (err) {
      message.error("Ошибка входа. Проверьте имя пользователя и пароль.");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "0 auto", padding: "20px" }}>
      <Title level={2}>Вход</Title>
      <Form layout="vertical">
        <Form.Item label="Имя пользователя" required>
          <Input
            placeholder="Имя пользователя"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </Form.Item>

        <Form.Item label="Пароль" required>
          <Input.Password
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Item>

        <Form.Item>
          <Button type="primary" onClick={handleLogin} block>
            Войти
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
