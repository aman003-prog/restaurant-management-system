import { createContext, useContext, useState, useEffect } from "react";
import { apiRequest } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("access_token") || null);
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("user_info");
    try {
      return savedUser ? JSON.parse(savedUser) : null;
    } catch {
      return null;
    }
  });

  useEffect(() => {
    if (token && !user) {
      apiRequest("/users/me/")
        .then((profile) => {
          setUser(profile);
          localStorage.setItem("user_info", JSON.stringify(profile));
        })
        .catch(() => {
          logout();
        });
    }
  }, [token]);

  const login = async (username, password) => {
    const data = await apiRequest("/auth/login/", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });

    localStorage.setItem("access_token", data.access);
    if (data.refresh) localStorage.setItem("refresh_token", data.refresh);
    setToken(data.access);

    const profile = await apiRequest("/users/me/", {
      headers: { Authorization: `Bearer ${data.access}` },
    });
    setUser(profile);
    localStorage.setItem("user_info", JSON.stringify(profile));
    return profile;
  };

  const register = async ({ username, email, password, password_confirm, phone_number }) => {
    await apiRequest("/auth/register/", {
      method: "POST",
      body: JSON.stringify({
        username,
        email,
        password,
        password_confirm,
        phone_number,
      }),
    });
    return login(username, password);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_info");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, isAuthenticated: !!token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within an AuthProvider");
  return context;
}
