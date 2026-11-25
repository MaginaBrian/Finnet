import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import * as authApi from "../api/auth";
import { configureClient } from "../api/client";

const AuthContext = createContext(null);
const TOKEN_KEY = "fintrack.token";

function readToken() {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

function writeToken(token) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  } catch {

  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(readToken);
  const [user, setUser] = useState(null);
  const [booting, setBooting] = useState(Boolean(readToken()));

  const logout = useCallback(() => {
    writeToken(null);
    setToken(null);
    setUser(null);
  }, []);

  useEffect(() => {
    configureClient({ getToken: () => token, onUnauthorized: logout });
  }, [token, logout]);

  useEffect(() => {
    if (!token || user) {
      setBooting(false);
      return;
    }
    const controller = new AbortController();
    authApi
      .fetchMe(controller.signal)
      .then((res) => setUser(res.user))
      .catch((err) => err.name !== "AbortError" && logout())
      .finally(() => setBooting(false));
    return () => controller.abort();

  }, [token]);

  const accept = useCallback((res) => {
    writeToken(res.token);
    configureClient({ getToken: () => res.token });
    setToken(res.token);
    setUser(res.user);
  }, []);

  const value = useMemo(
    () => ({
      user,
      token,
      booting,
      isAuthenticated: Boolean(token),
      login: async (username, password) => accept(await authApi.login(username, password)),
      register: async (username, password, fullName) =>
        accept(await authApi.register(username, password, fullName)),
      logout,
    }),
    [user, token, booting, accept, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
