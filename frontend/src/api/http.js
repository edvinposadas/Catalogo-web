import axios from "axios";

const API_URL = "http://127.0.0.1:5000/api";

const http = axios.create({
  baseURL: API_URL,
  withCredentials: true, // necesario para cookies (refresh)
});

// Inyectar access_token en cada request
http.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("access_token");
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para refrescar access_token automáticamente
http.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config || {};
    // si no hay respuesta (network/CORS), rechaza
    if (!error.response) return Promise.reject(error);

    if (error.response.status === 401 && !original._retry) {
      original._retry = true;
      try {
        // refresh sin interceptores, pero con credenciales (cookie httpOnly)
        const r = await axios.post(`${API_URL}/auth/refresh`, {}, { withCredentials: true });
        const newAccess = r.data.access_token;

        // 👉 usa sessionStorage (no localStorage) para mantener el comportamiento de sesión
        sessionStorage.setItem("access_token", newAccess);

        original.headers = original.headers || {};
        original.headers.Authorization = `Bearer ${newAccess}`;
        return http.request(original);
      } catch (e) {
        // limpiar sesión y redirigir a login
        sessionStorage.removeItem("access_token");
        sessionStorage.removeItem("username");
        window.location.href = "/login";
        return Promise.reject(e);
      }
    }
    return Promise.reject(error);
  }
);

export default http;
export { API_URL };
