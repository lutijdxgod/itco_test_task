import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { Button, Input, Form, message, Typography } from "antd";

const { Title } = Typography;

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    try {
      await api.post("/auth/register", { username, password });
      message.success("Регистрация прошла успешно! Переходите к входу.");
      navigate("/login");
    } catch (err) {
      if (err.response?.status === 403) {
        setError("Пользователь уже существует");
        message.error("Пользователь с таким именем уже существует");
      } else {
        setError("Ошибка регистрации");
        message.error("Ошибка регистрации");
      }
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "0 auto", padding: "20px" }}>
      <Title level={2}>Регистрация</Title>
      <Form layout="vertical">
        <Form.Item
          label="Имя пользователя"
          name="username"
          rules={[
            {
              required: true,
              message: "Введите имя пользователя.",
            },
          ]}
        >
          <Input
            placeholder="Имя пользователя"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </Form.Item>

        <Form.Item
          label="Пароль"
          name="password"
          rules={[{ required: true, message: "Введите пароль." }]}
        >
          <Input.Password
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Item>

        <Form.Item>
          <Button type="primary" onClick={handleRegister} block>
            Зарегистрироваться
          </Button>
        </Form.Item>
      </Form>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
