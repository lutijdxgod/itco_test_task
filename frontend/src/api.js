import axios from "axios";
import { getToken } from "./auth";

const api = axios.create({ baseURL: "http://localhost:8000" });

const authRoutes = ["/auth/login", "/auth/register"];

api.interceptors.request.use(
  (config) => {
    const isAuthRoute = authRoutes.some((route) => config.url.includes(route));

    if (!isAuthRoute) {
      const token = getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
