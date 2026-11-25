import { createContext, useEffect, useMemo, useState } from "react";
import * as authApi from "../api/authApi";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setLoading(false);
      return;
    }
    authApi
      .fetchMe()
      .then(setUser)
      .catch(() => {
        localStorage.removeItem("token");
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const value = useMemo(
    () => ({
      user,
      loading,
      async login(username, password) {
        const result = await authApi.login({ username, password });
        localStorage.setItem("token", result.token);
        setUser(result.user);
        return result.user;
      },
      async register(username, fullName, password) {
        const result = await authApi.register({
          username,
          full_name: fullName,
          password,
        });
        localStorage.setItem("token", result.token);
        setUser(result.user);
        return result.user;
      },
      logout() {
        localStorage.removeItem("token");
        setUser(null);
      },
    }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
